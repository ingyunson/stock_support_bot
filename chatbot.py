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

dir = '/root/chatbot/stock/'
today_finance = pd.read_csv(dir+'{}_KRX_finance.csv'.format(nowDate), dtype={'code':str})
today_stock = pd.read_csv(dir+'{}_KRX_stock.csv'.format(nowDate), dtype={'code':str})

user = pd.DataFrame(columns = ['User_id', '자본유보율', '연매출', '부채비율', 'PER', 'PBR', 'ROIC', 'ROE', 'BPS', 'EPS', '수익률'])
userdata = pd.read_csv(dir+'user_db.csv')
del userdata['Unnamed: 0']

today = pd.merge(today_finance, today_stock, on = "name")
today = today.drop_duplicates()
today = today.reset_index(drop = True)
del today['Unnamed: 0_x']
del today['Unnamed: 0_y']
del today['date_y']
del today['code_y']

today[['자본유보율', '연매출', '자기자본(자본총계)', '자본금', '부채비율', 'PER', 'PBR', 'BPS', 'EPS', '52_high', '52_low', 'price', 'ROA', 'ROE', 'ROIC']] = today[['자본유보율', '연매출', '자기자본(자본총계)', '자본금', '부채비율', 'PER', 'PBR', 'BPS', 'EPS', '52_high', '52_low', 'price', 'ROA', 'ROE', 'ROIC']].apply(pd.to_numeric)

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

def send_message():
    for i in range(len(userdata)):
        data = []
        for index in userdata:
            get = (userdata.loc[i][index])
            data.append(get)
        today['BPS_mul'] = today['BPS'] * data[8]
        today['EPS_mul'] = today['EPS'] * data[9]
        today['low'] = today[['BPS_mul', 'EPS_mul']].min(axis=1)
        today['A'] = today['low'] * data[10] / 100
        today['mark'] = ((today['low'] + today['A']) < today['52_high']) & (
                    (today['low'] - today['A']) < today['price'])
        today['special'] = ((today['low'] + today['A']) < today['52_low']) & (
                    (today['low'] - today['A']) < today['price'])

        result = today[(today['자본유보율'] > data[1]) & (today['연매출'] > data[2]) & (today['부채비율'] < data[3]) & (
                    (((today['자본금'] - today['자기자본(자본총계)']) / today['자본금']) * 100) < 0) & (today['PER'] < data[4]) & (
                                   today['PBR'] < data[5]) & (today['ROIC'] > data[6]) & (
                                   today['ROIC'] > today['ROA']) & (today['ROE'] > data[7]) & (today['mark'] == True)]
        name = []
        code = []
        message = ['{}의 선정 주식은 다음과 같습니다.'.format(nowDate)]
        name.append(result['name'].values)
        code.append(result['code_x'].values)
        for num in range(len(name[0])):
            note = "기업명 : {name}\nURL : https://finance.naver.com/item/main.nhn?code={code}".format(name=name[0][num],
                                                                                                    code=code[0][num])
            message.append(note)
        final = '\n\n'.join(message)
    for id in userdata['User_id']:
        try:
            bot.sendMessage(chat_id=id, text=final)
        except:
            bot.sendMessage(chat_id = 68008527, text = id)


send_message()

#print('chatbot is ready')
start_handler = CommandHandler('start', start_command)
join_handler = CommandHandler('join', join_command)
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(join_handler)

#updater.start_polling()
#updater.idle()
