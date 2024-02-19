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








def extract_race_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    race_info_list = []

    for race_line in soup.select('.kcup_list .line'):
        block = race_line.select_one('.block div').text.strip()
        place = race_line.select_one('.place div p:nth-child(2)').text.strip()
        days = race_line.select_one('.days div').get_text(separator=' ').strip()

        race_info = {
            "ブロック": block,
            "会場": place,
            "日程": days
        }
        race_info_list.append(race_info)

    return race_info_list

def main():
    st.title("レーススケジュール")

    # 対象のHTMLページのURLを入力
    url = st.text_input("HTMLページのURLを入力してください")

    if st.button("スケジュール取得"):
        # HTMLを取得
        response = requests.get(url)

        if response.status_code == 200:
            # レース情報を取得
            race_info_list = extract_race_info(response.text)

            # テーブルで表示
            st.table(race_info_list)
        else:
            st.error("ページの取得に失敗しました。URLを確認してください。")

if __name__ == "__main__":
    main()
