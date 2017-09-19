import re

from config import *


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    uid = m.from_user.id
    username = m.chat.username
    first_name = m.chat.first_name
    last_name = m.chat.last_name
    if is_registered(cid):
        bot.reply_to(m, "Пришли мне форвард /top из @ChatWarsBot")
    else:
        register_user(cid, username, first_name, last_name)
        bot.reply_to(m, "Привет!\nМы собираем топ всех игроков игры ChatWars.\nПришли мне форвард /top из @ChatWarsBot")


@bot.message_handler(commands=['top'])
def command_start(m):
    get_rating(m.chat.id)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if is_forward_from_cw(message):
        top_text = str(message.text)
        top_text = top_text[top_text.find("#"):].replace("...\n", "")
        for char in trash_symbols:
            top_text = top_text.replace(char, '')
        slices = top_text.split("\n")
        for i in slices:
            r = re.search("(#\s\d+) (.+(?= \d))", i)
            position = r.group(1).strip("#, ")
            name = r.group(2).strip()
            fraction = re.findall(r'[^\w\s,]', name)
            fraction = ''.join(fraction).strip("-, ")
            name = name.replace(fraction, "")
            print(position + name + flags[fraction])
            update_rating(name, position, flags[fraction])
        bot.send_message(message.chat.id, "Спасибо. Теперь можешь посмотреть общий рейтинг по /top")
    else:
        bot.send_message(message.chat.id, "Принимаем только форварды из @ChatWarsBot")
