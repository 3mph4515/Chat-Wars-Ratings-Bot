# -*- coding: utf-8 -*-
import time

import importdir
from config import *

importdir.do('plugins', globals())
bot.polling(none_stop=False, interval=0, timeout=20)
start_date = datetime.datetime.fromtimestamp(int(round(time.time()))).strftime('%b, %d %H:%M')
print("Bot is running...")
