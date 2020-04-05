from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import requests
from bs4 import BeautifulSoup

from config import TG_TOKEN
from config import TG_API_URL 
from config import URL 

from main import parse
#from main import get_content
#REQUEST_KWARGS={
    # "USERNAME:PASSWORD@" is optional, if you need authentication:
 #   'proxy_url': 'http://257199291:VGoM70hz@orbtl.s5.opennetwork.cc:999/',
#}

import logging

def start (update, context):
    result = parse()

    if len(result) >= 50:
        for x in range (0, len(result), 10):
            update.message.reply_text(f'{str(result[x:x+5])}')
    else:
        update.message.reply_text(result)


def main():
    bot = Bot(
        token = TG_TOKEN,
        base_url=TG_API_URL,
    )
    updater = Updater(
        bot = bot,
        use_context=True,
        #request_kwargs=REQUEST_KWARGS
    )

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__': 
    logging.info('msg')
    main()    
    

