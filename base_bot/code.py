from defs import defs
from client import Client
import rooms
from collections import OrderedDict
import values
from user import user
from library import *

bot = defs(values.bot_token())

for message in bot.get_message():
    main_page(user(message['from']))