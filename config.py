import datetime
import telebot
from pymongo import MongoClient
from telebot import util

import botan
import secret

token = secret.bot_token
botan_token = secret.botan_token
original_cw_bot = 'ChatWarsBot'
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


def update_rating(name, position, fraction, time, level, xp):
    if db_rating.rating.find_one({"position": position}) is not None:
        db_rating.rating.update_one({
            "position": position
        }, {
            '$set': {
                "fraction": str(fraction),
                "name": str(name),
                "update_time": time,
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
                "update_time": time,
                "level": level,
                "xp": xp}
        }, upsert=False)
    else:
        db_rating.rating.insert_one({
            "name": str(name),
            "fraction": str(fraction),
            "position": position,
            "update_time": time,
            "level": level,
            "xp": xp
        })


def get_rating(chat_id):
    arr = []
    for i in db_rating.rating.find({}):
        name, fraction, position = i['name'], i['fraction'], i['position']
        update_time = i.get('update_time', 0)
        level = i.get('level', 0)
        xp = i.get('xp', 0)
        arr.append({'name': name, 'fraction': fraction, 'position': int(position),
                    'update_time': int(update_time), 'level': int(level), 'xp': int(xp), })
    arr = sorted(arr, key=lambda pos: pos['position'], reverse=False)
    text_to_send = "Текущий топ игроков:\n"
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
                        + "  " + format(level) + "  " + format(xp) + "  " + format(update_time) + "\n"
    try:
        if len(text_to_send) > 3000:
            splitted_text = util.split_string(text_to_send, 3000)
            for text in splitted_text:
                bot.send_message(chat_id, text)
        else:
            bot.send_message(chat_id, text_to_send)
    except Exception as e:
        print(e)


def get_flag(value):
    return list(flags.keys())[list(flags.values()).index(value)]
