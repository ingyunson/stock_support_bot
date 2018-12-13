import pandas as pd
import datetime

now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d')

today_finance = pd.read_csv('{}_KRX_finance.csv'.format(nowDate))
today_stock = pd.read_csv('{}_KRX_stock.csv'.format(nowDate))

