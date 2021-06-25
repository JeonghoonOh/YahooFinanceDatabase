import mysql.connector
import mysql
import pandas as pd
import requests
import pycountry
import re
import json
import csv
import time
import datetime
from io import StringIO
from bs4 import BeautifulSoup

# starting period is 20 years from today
# end period is set to current date.
period2 = int(time.mktime(datetime.date.today().timetuple()))
period1 = int(time.mktime((datetime.date.today()-datetime.timedelta(days=365*20)).timetuple()))

url_stats = "https://finance.yahoo.com/quote/{}/key-statistics?p={}"
url_profile = "https://finance.yahoo.com/quote/{}/profile?p={}"
url_financials = "https://finance.yahoo.com/quote/{}/financials?p={}"

stock = 'TSLA' # manually set this.

stock_profile = url_profile.format(stock,stock)
response = requests.get(stock_profile)
soup = BeautifulSoup(response.text, 'html.parser')
profile_data = soup.find('p',{"class":"D(ib) W(47.727%) Pend(40px)"}).contents
country = profile_data[9]

# 1 : 도로명 / 5: 시/주/우편번호/ 9: 국가명
country_code = pycountry.countries.get(name=country).alpha_2
print(country_code)
# soup = BeautifulSoup(url_profile.format(stock,stock), 'html.parser')
# print(soup.find_all('p'))

#column list for history data
colList_hist = ['Date','Open','High','Low','Close','Adj','Close','Volume']
query =  f'https://query1.finance.yahoo.com/v7/finance/download/{stock}?period1={period1}&period2={period2}&interval=1d&events=history&includeAdjustedClose=true'
df = pd.read_csv(query)

# connecting to mysql database
cnx = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root"
)
cursor = cnx.cursor()
cursor.execute("USE yahoo_stock")
cursor.execute("INSERT IGNORE INTO stock_info (ticker, country) VALUES(%(ticker)s,'US')",{'ticker': stock})
cnx.commit()
# params = {
#     'access_key': '1ab1cd73a675c61d7c7ac86428cc55df'
# }
#
# response = requests.get("http://api.marketstack.com/v1/eod?access_key=1ab1cd73a675c61d7c7ac86428cc55df&symbols=MSFT",
#                         params)
# print(response.json())