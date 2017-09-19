import telebot
from pymongo import MongoClient

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


def update_rating(name, position, fraction):
    if db_rating.rating.find_one({"position": position}) is not None:
        db_rating.rating.update_one({
            "position": position
        }, {
            '$set': {
                "fraction": str(fraction),
                "name": str(name)}
        }, upsert=False)
    elif db_rating.rating.find_one({"name": name}) is not None:
        print("Already exists")
        db_rating.rating.update_one({
            "name": name
        }, {
            '$set': {
                "fraction": str(fraction),
                "position": position}
        }, upsert=False)
    else:
        db_rating.rating.insert_one({
            "name": str(name),
            "fraction": str(fraction),
            "position": position,
        })


def get_rating(chat_id):
    arr = []
    for document in db_rating.rating.find({}):
        print(document)
        name, fraction, position = document['name'], document['fraction'], document['position']
        arr.append({'name': name, 'fraction': fraction, 'position': int(position)})
        # bot.send_message(chat_id, "")
    arr = sorted(arr, key=lambda pos: pos['position'], reverse=False)
    print(str(arr))
    res = "Top:\n"
    for i in arr:
        res += '%5s' % str(i['position']) + " " + get_flag_by_value(i['fraction']) + " " + str(i['name']) + "\n"
    bot.send_message(chat_id, res)


def get_flag_by_value(value):
    return list(flags.keys())[list(flags.values()).index(value)]
