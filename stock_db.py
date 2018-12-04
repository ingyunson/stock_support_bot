import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import datetime
import re
import json


code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
code_df = code_df[['회사명', '종목코드']]

# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})


# 종목 이름을 입력하면 종목에 해당하는 코드를 불러와
# 네이버 금융(http://finance.naver.com)에 넣어줌

def get_url(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    url = 'https://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={code}&cn='.format(code=code)

    print("요청 URL = {}".format(url))
    return url

def get_json(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    url = 'https://companyinfo.stock.naver.com/v1/company/c1040001.aspx?cmp_cd={code}'.format(code=code)
    html_text = requests.get(url).text
    encparam = re.findall("encparam: '(.*?)'", html_text)[0]
    url_json = 'https://companyinfo.stock.naver.com/v1/company/cF4002.aspx?cmp_cd={code}&frq=0&rpt=1&finGubun=MAIN&frqTyp=0&cn=&encparam={encparam}'.format(code=code, encparam=encparam)
    header = {'Referer': 'https://companyinfo.stock.naver.com/v1/company/c1040001.aspx',}
    html_text = requests.get(url_json, headers=header).text
    data = json.loads(html_text)

    print("요청 URL = {}".format(url))
    return data

def get_html(url):
    f = requests.get(url)
    soup = bs(f.text, 'html.parser')
    return soup

def get_param(url):
    html = requests.get(url).text
    encparam = re.findall("encparam: '(.*?)'", html)[0]
    encid = re.findall("id: '(.*?)'", html)[0]
    print(encparam)
    print(encid)

    return encparam, encid


# 입력한 주식의 일자데이터 url 가져오기
item_name = '셀트리온'

url1 = get_url(item_name, code_df)

# 일자 데이터를 담을 df라는 DataFrame 정의
df = pd.DataFrame()
df_stock = pd.DataFrame()
data = []
date = datetime.date.today()
name = item_name
code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
parse1 = get_html(url1)
PER = float(parse1.select('#pArea > div.wrapper-table > div > table > tr:nth-of-type(3) > td > dl > dt:nth-of-type(3) > b')[0].text)
PBR = float(parse1.select('#pArea > div.wrapper-table > div > table > tr:nth-of-type(3) > td > dl > dt:nth-of-type(5) > b')[0].text)
BPS = float(parse1.select('#pArea > div.wrapper-table > div > table > tr:nth-of-type(3) > td > dl > dt:nth-of-type(2) > b')[0].text.replace(',', ''))
EPS = float(parse1.select('#pArea > div.wrapper-table > div > table > tr:nth-of-type(3) > td > dl > dt:nth-of-type(1) > b')[0].text.replace(',', ''))
high = float(parse1.select('#cTB11 > tbody > tr:nth-of-type(2) > td')[0].get_text().strip().replace('\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t', '').replace(' ', '').replace('원', '').replace(',', '').split('/')[0])
low = float(parse1.select('#cTB11 > tbody > tr:nth-of-type(2) > td')[0].get_text().strip().replace('\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t', '').replace(' ', '').replace('원', '').replace(',', '').split('/')[1])
price = float(parse1.select('#cTB11 > tbody > tr:nth-of-type(1) > td > strong')[0].get_text().strip().replace(',', ''))
json_table = get_json(item_name, code_df)
ROE = json_table["DATA"][12]["DATA5"]
ROA = json_table["DATA"][16]["DATA5"]
ROIC = json_table["DATA"][20]["DATA5"]

data.extend((date, name, code, PER, PBR, BPS, EPS, high, low, price, ROA, ROE, ROIC))
print(data)




# df_stock = df.rename(columns = ['date', 'name', 'code', 'PER', 'PBR', 'BPS', 'EPS', '52_high', '52_low', 'price', 'ROA', 'ROE', 'ROIC'])



