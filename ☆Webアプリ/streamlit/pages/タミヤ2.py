import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

# タミヤニュースレースイベントのWebページを解析する関数
def parse_tamiya_news():
    url = 'https://www.tamiya.com/japan/event/index.html?genre_item=event_rc,event_type,kinki&sortkey=sa'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    
    # タミヤニュースレースイベントの内容をclass属性で検索（都度変更が必要）
    topic = soup.find(class_='category_event_ event_calendar_')
    
    news_text = [i.text for i in topic.find_all('a')]
    news_link = [i.get('href') for i in topic.find_all('a')]
    
    return news_text, news_link

# Streamlitアプリケーションの開始
st.title('タミヤレースサイト見出し')

# タミヤニュースを解析してデータを取得
news_text, news_link = parse_tamiya_news()

# ハイパーリンクを表示する
st.write('## ニュース一覧')
df_display = pd.DataFrame({'主要ニュース': news_text, 'リンク': news_link})
df_display['リンク'] = df_display['リンク'].apply(lambda x: f"[{x}]({x})")
st.write(df_display)
