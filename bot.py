from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import requests
from bs4 import BeautifulSoup
import re

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
    
    split_regex = re.compile(r'[{|}]')
    sentences = filter(lambda t: t, [t.strip() for t in split_regex.split(result)])
    for s in sentences:
        update.message.reply_text(f'{s}')


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
    

