import pandas as pd
import datetime
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d')

my_token = <CHATBOT TOKEN>
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

def send_message():
    for i in range(len(userdata)):
        data = []
        for index in userdata:
            get = (userdata.loc[i][index])
            data.append(get)
        today['BPS_mul'] = today['BPS'] * data[8]
        today['EPS_mul'] = today['EPS'] * data[9]
        today['low'] = today[['BPS_mul', 'EPS_mul']].min(axis=1)
        today['sell'] = today['low'] * (20 / 100) #data[10]
        today['buy'] = today['low'] * (5 / 100) #data[11] : 아직 설정하지 않음
        today['sell_estimate'] = today['low'] + today['sell']
        today['buy_estimate'] = today['low'] - today['buy']
        today['mark'] = ((today['low'] + today['sell']) < today['52_high']) & (
                    (today['low'] - today['buy']) < today['price'])
        today['special'] = ((today['low'] + today['sell']) < today['52_low']) & (
                    (today['low'] - today['buy']) < today['price'])
        result = today[(today['자본유보율'] > data[1]) & (today['연매출'] > data[2]) & (today['부채비율'] < data[3]) & (
                    (((today['자본금'] - today['자기자본(자본총계)']) / today['자본금']) * 100) < 0) & (today['PER'] < data[4]) & (
                                   today['PBR'] < data[5]) & (today['ROIC'] > data[6]) & (
                                   today['ROIC'] > today['ROA']) & (today['ROE'] > data[7]) & (today['mark'] == True)]
        name = []
        code = []
        price = []
        sell_estimate = []
        buy_estimate = []
        final = []
        message = ['{}의 선정 주식은 다음과 같습니다.'.format(nowDate)]
        name.append(result['name'].values)
        code.append(result['code_x'].values)
        price.append(result['price'].values)
        sell_estimate.append(result['sell_estimate'].values)
        buy_estimate.append(result['buy_estimate'].values)
        for num in range(len(name[0])):
            note = "기업명 : {name}\nURL : https://finance.naver.com/item/main.nhn?code={code}\n전일종가 : {price}\n매수 적정가 : {buy_estimate}\n매도 적정가 : {sell_estimate}".format(
                name=name[0][num], code=code[0][num], price=price[0][num], sell_estimate=sell_estimate[0][num],
                buy_estimate=buy_estimate[0][num])
            message.append(note)
        if len(message) > 20:
            temp_1 = '\n\n'.join(message[:20])
            temp_2 = '\n\n'.join(message[20:])
            final.append(temp_1)
            final.append(temp_2)
        else:
            temp = '\n\n'.join(message)
            final.append(temp)

        user_id = str(userdata.loc[i]['User_id'])
        print(user_id)

        try:
            for i in range(len(final)):
                bot.sendMessage(chat_id=user_id, text=final[i])
        except Exception as e:
            bot.sendMessage(chat_id=<ADMIN CHAT ID>, text=id + e)


send_message()


