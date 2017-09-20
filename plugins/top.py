import time
import re

from config import *

FORWARD_EXPIRE_TIME_IN_SECONDS = 120


@bot.message_handler(commands=['top'])
def command_start(m):
    get_rating(m.chat.id)


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
            print(position + name + flags[fraction] + level + xp)
            update_rating(name, position, flags[fraction], current_millis, level, xp)
        bot.send_message(message.chat.id, "Спасибо. Теперь можешь посмотреть общий рейтинг по /top")
    else:
        bot.send_message(message.chat.id, "Принимаем только форварды /top из @ChatWarsBot")
