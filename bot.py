from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from bs4 import BeautifulSoup
import re
import requests
import logging

from config import TG_TOKEN
from config import TG_API_URL 
from config import URL 
from main import parse

def start (update, context):
    result = parse()
    to_string = ''.join(result).replace("'", '')
    update.message.reply_text(to_string)

    try:
        pattern = re.compile(r'[{|}}]')
        sentences = filter(lambda t: t, [t.strip() for t in pattern.split(to_string)])
        for s in sentences:
            update.message.reply_text(f'{s}')
    except:
        update.message.reply_text(result)

def main():
    bot = Bot(
        token = TG_TOKEN,
        base_url=TG_API_URL,
    )
    updater = Updater(
        bot = bot,
        use_context=True
    )
    #job = updater.job_queue.run_repeating(start, 60, 0)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__': 
    logging.info('msg')
    main()    
    

