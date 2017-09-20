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
