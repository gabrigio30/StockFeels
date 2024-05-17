from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import certifi

finviz_url = 'https://finviz.com/quote.ashx?t='
tickers = ['AMZN', 'FB', 'AMD']

#in this variable we will store the tables of news for each stock we want to analyze
news_tables = {}

for ticker in tickers:
    url = finviz_url + ticker

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req, cafile=certifi.where())
    
    html = BeautifulSoup(response, features='html.parser')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table
    break

#we will parse the table row singularly to analyze it
amzn_data = news_tables['AMZN']
amzn_rows = amzn_data.find_all('tr')

for index, row in enumerate(amzn_rows):
    title = row.a.text
    timestamp = row.td.text
    print(timestamp + ' ' + title)

parsed_data = []

for ticker, news_table in news_tables.items():
    for row in news_table.findAll('tr'):
        title = row.a.text
        date_data = row.td.text.split(' ')
        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker, date, time, title])

print(parsed_data)