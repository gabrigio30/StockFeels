from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import date
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import certifi
import ssl
import matplotlib.pyplot as plt

finviz_url = 'https://finviz.com/quote.ashx?t='
tickers = ['AMZN', 'GOOG', 'AAPL', 'NVDA']

#in this variable we will store the tables of news for each stock we want to analyze
news_tables = {}

for ticker in tickers:
    url = finviz_url + ticker
    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req, context=ssl.create_default_context(cafile=certifi.where()))
    html = BeautifulSoup(response, features='html.parser')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

parsed_data = []
time = ''
day = ''

for ticker, news_table in news_tables.items():
    for row in news_table.findAll('tr'):
        title = row.a.text
        date_data = row.td.text.split()

        if len(date_data)==1:
            time = date_data[0]
        else:
            day = date_data[0]
            time = date_data[1]

        if day == 'Today':
            day = date.today()

        parsed_data.append([ticker, day, time, title])

df = pd.DataFrame(parsed_data, columns=['ticker', 'day', 'time', 'title'])
vader = SentimentIntensityAnalyzer()

score = lambda title: vader.polarity_scores(title)['compound']
df['compound'] = df['title'].apply(score)
df['day'] = pd.to_datetime(df.day).dt.date
#each website page contains up to 100 articles on the specified ticker

mean_df = df.groupby(['ticker', 'day']).mean(['compound'])
mean_df = mean_df.unstack()
mean_df = mean_df.xs('compound', axis='columns').transpose()
mean_df.plot(kind='bar')
plt.show()
