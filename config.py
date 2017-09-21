import datetime
import telebot
from pymongo import MongoClient
from telebot import util

import botan
import secret
import time

token = secret.bot_token
botan_token = secret.botan_token
original_cw_bot = 'ChatsWarBot'
trash_symbols = ['🏅', '👑']
bot = telebot.TeleBot(token)
client = MongoClient('localhost:27017')
db = client.users
db_rating = client.rating

userStep = dict()
flags = {
    '🇪🇺': 'blue',
    '🇮🇲': 'red',
    '🇬🇵': 'black',
    '🇻🇦': 'yellow',
    '🇨🇾': 'white',
    '🇰🇮': 'twilight',
    '🇲🇴': 'mint',
    '❌': 'deleted'
}


def track_new_user(uid):
    print(botan.track(botan_token, uid, {'text': 2}, 'New User'))


def is_forward_from_cw(message):
    if hasattr(message.forward_from, 'username') and message.forward_from.username == original_cw_bot:
        return True
    else:
        return False


def is_registered(cid):
    return db.users.find_one(str(cid)) is not None


def register_user(cid, name, first_name, last_name):
    db.users.insert_one({
        "_id": str(cid),
        "name": str(name),
        "first_name": str(first_name),
        "last_name": str(last_name),
        "banned": False,
        "notify": True,
    })


def update_rating(name, position, fraction, update_time, level, xp):
    if db_rating.rating.find_one({"position": position}) is not None:
        dups = db_rating.rating.find({"name": name})
        for dup in dups:
            db_rating.rating.delete_one({"_id": dup['_id']})
        db_rating.rating.update_one({
            "position": position
        }, {
            '$set': {
                "fraction": str(fraction),
                "name": str(name),
                "update_time": update_time,
                "level": level,
                "xp": xp
            }
        }, upsert=False)
    elif db_rating.rating.find_one({"name": name}) is not None:
        db_rating.rating.update_one({
            "name": name
        }, {
            '$set': {
                "fraction": str(fraction),
                "position": position,
                "update_time": update_time,
                "level": level,
                "xp": xp}
        }, upsert=False)
    else:
        db_rating.rating.insert_one({
            "name": str(name),
            "fraction": str(fraction),
            "position": position,
            "update_time": update_time,
            "level": level,
            "xp": xp
        })


def get_rating(chat_id):
    arr = []
    count_table = {'red': 0, 'blue': 0, 'mint': 0, 'twilight': 0, 'deleted': 0, 'black': 0, 'white': 0, 'yellow': 0}
    for i in db_rating.rating.find({}):
        name, fraction, position = i['name'], i['fraction'], i['position']
        update_time = i.get('update_time', 0)
        level = i.get('level', 0)
        xp = i.get('xp', 0)
        count_table[fraction] += 1
        if int(level) >= 50:
            arr.append({'name': name, 'fraction': fraction, 'position': int(position),
                        'update_time': int(update_time), 'level': int(level), 'xp': int(xp), })
    arr = sorted(arr, key=lambda pos: pos['position'], reverse=False)
    text_to_send = "Текущий топ игроков:(Временно урезано до минимального уровня 40)\n"
    for i in arr:
        update_time = ""
        level = ""
        xp = ""
        if int(i['update_time']) > 0:
            update_time = datetime.datetime.fromtimestamp(int(i['update_time'])).strftime('%b, %d %H:%M')
        if int(i['level']) > 0:
            level = i['level']
        if int(i['xp']) > 0:
            xp = i['xp']
        text_to_send += '{:5}'.format(i['position']) + "  " + get_flag(i['fraction']) + "  " + i['name'] \
                        + "  " + format(level) + "  " + format(xp) + "\n"
    text_to_send += "\nВсего красных: " + format(
        count_table['red']) + "\nВсего синих: " + format(
        count_table['blue']) + "\nВсего желтых: " + format(
        count_table['yellow']) + "\nВсего черных: " + format(
        count_table['black']) + "\nВсего мятных: " + format(
        count_table['mint']) + "\nВсего сумрачных: " + format(
        count_table['twilight']) + "\nВсего белых: " + format(
        count_table['white']) + "\nВсего забанено: " + format(
        count_table['deleted'])
    try:
        if len(text_to_send) > 3999:
            splitted_text = util.split_string(text_to_send, 3999)
            for text in splitted_text:
                bot.send_message(chat_id, text)
                time.sleep(0.5)
        else:
            bot.send_message(chat_id, text_to_send)

    except Exception as e:
        print(e)


def get_flag(value):
    return list(flags.keys())[list(flags.values()).index(value)]


# Run for debug only
def remove_duplicates():
    removed = 0
    for i in db_rating.rating.find({}):
        name = i['name']
        xp = i['xp']
        _id = i['_id']
        for j in db_rating.rating.find({}):
            _id2 = j['_id']
            if str(_id2) != str(_id) and j['name'] == name and int(xp) > int(j['xp']):
                removed += 1
                db_rating.rating.delete_one({"_id": j['_id']})
    print("Removed " + str(removed))
