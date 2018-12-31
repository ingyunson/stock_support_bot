import pandas as pd
import datetime
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d')

my_token = '729504243:AAFQEqyGx_yjOkSEBoNCUToP2KLH0VR-WX4'
bot = telegram.Bot(token = my_token)   #bot을 선언합니다.

updater = Updater(my_token)
updates = bot.getUpdates()  #업데이트 내역을 받아옵니다.


def start_command(bot, update):
    print("start")
    update.message.reply_text("주식 투자 보조용 챗봇입니다.\n'/join' 혹은 '/시작'을 입력하시면 정보를 등록합니다.")

#print('chatbot is ready')
start_handler = CommandHandler('start', start_command)
updater.dispatcher.add_handler(start_handler)

#updater.start_polling()
#updater.idle()