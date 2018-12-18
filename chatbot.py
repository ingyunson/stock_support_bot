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

today_finance = pd.read_csv('KRX_finance.csv'.format(nowDate))
today_stock = pd.read_csv('KRX_stock.csv'.format(nowDate))

finance_condition = [100, 100, 100] #자본유보율, 연매출, 부채비율 조건 조정
stock_condition = [10, 10, 10, 10, 10, 10, 10, 10] #PER, PBR, ROIC, ROE, BPS, EPS, 수익율 조절 가능
user = pd.DataFrame(columns = ['User_id', '자본유보율', '연매출', '부채비율', 'PER', 'PBR', 'ROIC', 'ROE', 'BPS', 'EPS', '수익률'])
userdata = pd.read_csv('test.csv')

today_stock['BPS_mul'] = today_stock['BPS'] * stock_condition[4]
today_stock['EPS_mul'] = today_stock['EPS'] * stock_condition[5]
today_stock['low'] = today_stock[['BPS_mul','EPS_mul']].min(axis=1)
today_stock['A'] = today_stock['low'] * stock_condition[6]/100
today_stock['mark'] = ((today_stock['low'] + today_stock['A']) < today_stock['52_high']) & ((today_stock['low'] - today_stock['A']) < today_stock['price'])
today_stock['special'] = ((today_stock['low'] + today_stock['A']) < today_stock['52_low']) & ((today_stock['low'] - today_stock['A']) < today_stock['price'])

today_finance[(today_finance['자본유보율'] > finance_condition[0]) & (today_finance['연매출'] > finance_condition[1]) & (today_finance['부채비율'] < finance_condition[2]) & ((((today_finance['자본금'] - today_finance['자기자본(자본총계)']) / today_finance['자본금'])*100) < 0)]
today_stock[(today_stock['PER'] < stock_condition[0]) & (today_stock['PBR'] < stock_condition[1]) & (today_stock['ROIC'] > stock_condition[2]) & (today_stock['ROIC'] > today_stock['ROA']) & (today_stock['ROE'] > stock_condition[3] ) & (today_stock['mark'] == True) ]


# 챗봇 part

# 자본유보율, 연매출, 부채비율 조건 조정
# PER, PBR, ROIC, ROE, BPS, EPS, 수익율
# user_info = [user_id, 자본유보율, 연매출, 부채비율, PER, PBR, ROIC, ROE, BPS, EPS, 수익률]

def start_command(bot, update):
    print("start")
    update.message.reply_text("주식 투자 보조용 챗봇입니다.\n'/join' 혹은 '/시작'을 입력하시면 정보를 등록합니다.")


def join_command(bot, update):
    user_id = bot.getUpdates()[-1].message.chat.id
    print(user_id)
    user_info = ['a', 100, 100, 100, 10, 10, 10, 10, 10, 10, 10]
    user_info[0] = user_id
    update.message.reply_text(
        "회원 정보를 등록합니다. 회원 정보 및 기본 설정은 다음과 같습니다.\nUser id = {id}\n자본유보율 = {cap}, 연매출 = {ben}, 부채비율 = {debt}\nPER = {per}, PBR = {pbr}, ROIC = {roic}, ROE = {roe}, BPS = {bps}, EPS = {eps}, 수익률 = {earn}".format(
            id=user_id, cap=user_info[1], ben=user_info[2], debt=user_info[3], per=user_info[4], pbr=user_info[5],
            roic=user_info[6], roe=user_info[7], bps=user_info[8], eps=user_info[9], earn=user_info[10]))




for id in userdata['User_id']:
    print(id)

print('chatbot is ready')
start_handler = CommandHandler('start', start_command)
join_handler = CommandHandler('join', join_command)
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(join_handler)

updater.start_polling()
updater.idle()
