import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import datetime

# YahooニュースのWebページを解析する関数
def parse_yahoo_news():
    url = 'https://news.yahoo.co.jp/'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    
    # Yahooニュース内の最新トピックスをclass属性で検索（都度変更が必要）
    topic = soup.find(class_='sc-jnrPYG eYSvJf')
    
    news_text = [i.text for i in topic.find_all('a')]
    news_link = [i.get('href') for i in topic.find_all('a')]
    
    return news_text, news_link

# Streamlitアプリケーションの開始
st.title('Yahooニュース見出し')

# Yahooニュースを解析してデータを取得
news_text, news_link = parse_yahoo_news()

# 取得したデータをDataFrameに格納
data = {'主要ニュース': news_text, 'リンク': news_link}
df = pd.DataFrame(data)

# データを表示する
st.write('## ニュース一覧')
st.write(df)











# タミヤニュースレースイベントのWebページを解析する関数
def parse_tamiya_news():
    tamiya_url = 'https://www.tamiya.com/japan/event/index.html?genre_item=event_rc,event_type,kinki&sortkey=sa'
    tamiya_html = requests.get(tamiya_url)
    tamiya_soup = BeautifulSoup(tamiya_html.content, 'html.parser')
    
    # タミヤニュースレースイベントの内容をclass属性で検索（都度変更が必要）
    tamiya_topic = tamiya_soup.find(class_='category_event_ event_calendar_')
    
    tamiya_news_text = [i.text for i in tamiya_topic.find_all('a')]
    tamiya_news_link = [i.get('href') for i in tamiya_topic.find_all('a')]
    
    return tamiya_news_text, tamiya_news_link

# Streamlitアプリケーションの開始
st.title('タミヤレースサイト見出し')

# Yahooニュースを解析してデータを取得
tamiya_news_text, tamiya_news_link = parse_tamiya_news()

# 取得したデータをDataFrameに格納
tamiya_data = {'主要ニュース': tamiya_news_text, 'リンク': tamiya_news_link}
tamiya_df = pd.DataFrame(tamiya_data)

# データを表示する
st.write('## ニュース一覧')
st.write(tamiya_df)



# kyoshoニュースレースイベントのWebページを解析する関数
def parse_kyosho_news():
    kyosho_url = 'https://www.kyosho.com/rc/ja/race/2024/kyosho_cup/index.html'
    kyosho_html = requests.get(kyosho_url)
    kyosho_soup = BeautifulSoup(kyosho_html.content, 'html.parser')
    
    # タミヤニュースレースイベントの内容をclass属性で検索（都度変更が必要）
    kyosho_topic = kyosho_soup.find(class_='contentsarea contentsarea2 ')
    
    kyosho_news_text = [i.text for i in kyosho_topic.find_all('place')]
    
    
    return kyosho_news_text, kyosho_news_link

# Streamlitアプリケーションの開始
st.title('京商レースサイト見出し')

# Yahooニュースを解析してデータを取得
kyosho_news_text, kyosho_news_link = parse_kyosho_news()

# 取得したデータをDataFrameに格納
kyosho_data = {'主要ニュース': kyosho_news_text, 'リンク': kyosho_news_link}
kyosho_df = pd.DataFrame(kyosho_data)

# データを表示する
st.write('## ニュース一覧')
st.write(kyosho_df)
