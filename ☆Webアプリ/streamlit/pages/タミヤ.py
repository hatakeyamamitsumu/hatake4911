import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import datetime

# YahooニュースのWebページを解析する関数
def parse_tamiya_news():
    url = 'https://www.tamiya.com/japan/event/index.html?genre_item=event_rc,event_type,kinki&sortkey=sa'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    
    # Yahooニュース内の最新トピックスをclass属性で検索（都度変更が必要）
    topic = soup.find(class_='category_event_ event_calendar_')
    
    news_text = [i.text for i in topic.find_all('a')]
    news_link = [i.get('href') for i in topic.find_all('a')]
    
    return news_text, news_link

# Streamlitアプリケーションの開始
st.title('タミヤサイト見出し')

# Yahooニュースを解析してデータを取得
news_text, news_link = parse_tamiya_news()

# 取得したデータをDataFrameに格納
data = {'主要ニュース': news_text, 'リンク': news_link}
df = pd.DataFrame(data)

# データを表示する
st.write('## ニュース一覧')
st.write(df)
