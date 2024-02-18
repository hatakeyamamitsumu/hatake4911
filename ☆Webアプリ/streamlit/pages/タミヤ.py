import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import datetime

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
