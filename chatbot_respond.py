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

userdata = pd.read_csv('user_db_test.csv')
del userdata['Unnamed: 0']


def start_command(bot, update):
    print("start")
    update.message.reply_text("주식 투자 보조용 챗봇입니다.\n'/join' 혹은 '/시작'을 입력하시면 정보를 등록합니다.")

#print('chatbot is ready')
start_handler = CommandHandler('start', start_command)
updater.dispatcher.add_handler(start_handler)

#updater.start_polling()
#updater.idle()

def modify(user_id, cap = 200, ben = 300, debt = 100, per = 5, pbr = 1, roic = 5, roe = 5, bps = 1, eps = 5, interest = 5):
    if user_id in userdata['User_id'].values:
        userdata.loc[userdata.User_id == user_id, '자본유보율'] = cap
        userdata.loc[userdata.User_id == user_id, '연매출'] = ben
        userdata.loc[userdata.User_id == user_id, '부채비율'] = debt
        userdata.loc[userdata.User_id == user_id, 'PER'] = per
        userdata.loc[userdata.User_id == user_id, 'PBR'] = pbr
        userdata.loc[userdata.User_id == user_id, 'ROIC'] = roic
        userdata.loc[userdata.User_id == user_id, 'ROE'] = roe
        userdata.loc[userdata.User_id == user_id, 'EPS'] = eps
        userdata.loc[userdata.User_id == user_id, '수익률'] = interest
    else:
        print('please add account')
    return userdata