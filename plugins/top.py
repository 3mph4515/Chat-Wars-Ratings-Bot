import time
import re

from config import *

FORWARD_EXPIRE_TIME_IN_SECONDS = 120


@bot.message_handler(regexp="top(.*)")
def command_start(m):
    r_full = re.search("top_(\d+)_(\d+)", str(m.text))
    r = re.search("top_(\d+)", str(m.text))
    if r_full:
        range_from = int(r_full.group(1))
        range_to = int(r_full.group(2))
        if range_from > range_to:
            range_to, range_from = range_from, range_to
        if range_from < 0 or range_to < 0:
            send_msg(m.chat.id, "Принимаются только положительные значения")
            return None
        get_rating(m.chat.id, range_from, range_to)
    elif r:
        range_to = int(r.group(1))
        if range_to < 0:
            send_msg(m.chat.id, "Принимаются только положительные значения")
            return None
        get_rating(m.chat.id, 1, range_to)
    else:
        send_msg(m.chat.id, "Пришли команду в формате /top_от_до.\nВерхняя граница опциональный параметр")


@bot.message_handler(content_types=["text"])
def handle_top_forward(message):
    if is_forward_from_cw(message) and "Топ игроков:" in message.text:
        current_millis = int(round(time.time()))
        if current_millis - message.forward_date > FORWARD_EXPIRE_TIME_IN_SECONDS:
            bot.send_message(message.chat.id, "Форвард устарел. Пришли актуальный")
            return None
        top_text = str(message.text)
        top_text = top_text[top_text.find("#"):].replace("...\n", "")
        for char in trash_symbols:
            top_text = top_text.replace(char, '')
        slices = top_text.split("\n")
        for i in slices:
            r = re.search("(#\s\d+) (.+(?= \d)) (\d+)(/)(\d+)", i)
            position = r.group(1).strip("#, ")
            name = r.group(2).strip()
            level = r.group(3).strip()
            xp = r.group(5).strip()
            fraction = re.findall(r'[^\w\s,]', name)
            fraction = ''.join(fraction).strip("-, ")
            name = name.replace(fraction, "")
            if fraction in flags:
                flag = flags[fraction]
            else:
                flag = 'deleted'
            update_rating(name, position, flag, current_millis, level, xp)
        try:
            bot.send_message(message.chat.id, "Спасибо. Теперь можешь посмотреть общий рейтинг по /top")
        except Exception as e:
            print(e)
    else:
        try:
            bot.send_message(message.chat.id, "Принимаем только форварды /top из @ChatWarsBot")
        except Exception as e:
            print(e)
