import pandas as pd
import datetime

now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d')

today_finance = pd.read_csv('{}_KRX_finance.csv'.format(nowDate))
today_stock = pd.read_csv('{}_KRX_stock.csv'.format(nowDate))

finance_condition = [100, 100, 100] #자본유보율, 연매출, 부채비율 조건 조정
stock_condition = [10, 10, 10, 10, 10, 10, 10, 10] #PER, PBR, ROIC, ROE, BPS, EPS, 수익율 조절 가능


today_stock['BPS_mul'] = today_stock['BPS'] * stock_condition[4]
today_stock['EPS_mul'] = today_stock['EPS'] * stock_condition[5]
today_stock['low'] = today_stock[['BPS_mul','EPS_mul']].min(axis=1)
today_stock['A'] = today_stock['low'] * stock_condition[6]/100
today_stock['mark'] = ((today_stock['low'] + today_stock['A']) < today_stock['52_high']) & ((today_stock['low'] - today_stock['A']) < today_stock['price'])
today_stock['special'] = ((today_stock['low'] + today_stock['A']) < today_stock['52_low']) & ((today_stock['low'] - today_stock['A']) < today_stock['price'])

today_finance[(today_finance['자본유보율'] > finance_condition[0]) & (today_finance['연매출'] > finance_condition[1]) & (today_finance['부채비율'] < finance_condition[2]) & ((((today_finance['자본금'] - today_finance['자기자본(자본총계)']) / today_finance['자본금'])*100) < 0)]
today_stock[(today_stock['PER'] < stock_condition[0]) & (today_stock['PBR'] < stock_condition[1]) & (today_stock['ROIC'] > stock_condition[2]) & (today_stock['ROIC'] > today_stock['ROA']) & (today_stock['ROE'] > stock_condition[3] ) & (today_stock['mark'] == True) ]