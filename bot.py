# -*- coding: utf-8 -*-
import importdir
from config import *

importdir.do('plugins', globals())
bot.polling()
