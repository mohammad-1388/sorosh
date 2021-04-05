from defs import defs
from values import bot_token
from user import user
from library import main_page

bot = defs(bot_token())

for message in bot.get_message():
    main_page(user(message['from']))
