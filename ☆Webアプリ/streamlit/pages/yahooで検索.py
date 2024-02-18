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
st.title('Yahooニュース解析アプリ')

# Yahooニュースを解析してデータを取得
news_text, news_link = parse_yahoo_news()

# 取得したデータをDataFrameに格納
data = {'主要ニュース': news_text, 'リンク': news_link}
df = pd.DataFrame(data)

# Excelファイルに保存する関数
def save_to_excel(df):
    d = datetime.datetime.now()
    ymd_hm = d.strftime('%Y%m%d_%H%M_')
    file_name = f'ニュース一覧_{ymd_hm}.xlsx'
    df.to_excel(file_name, index=False)
    return file_name

# データを表示する
st.write('## ニュース一覧')
st.write(df)

# Excelファイルに保存するボタン
if st.button('Excelファイルに保存'):
    file_name = save_to_excel(df)
    st.success(f'ファイル "{file_name}" に保存しました。')





