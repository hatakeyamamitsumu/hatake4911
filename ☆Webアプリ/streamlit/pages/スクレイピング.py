import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# CSVファイルからエリアコードを取得する関数
def get_area_codes(csv_path):
    df = pd.read_csv(csv_path)
    return df["コード"].tolist()

# Yahoo天気予報をスクレイピングする関数
def GetYahooWeather(area_code):
    url = f"https://weather.yahoo.co.jp/weather/jp/13/{area_code}.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    rs = soup.find(class_='forecastCity')
    rs = [i.strip() for i in rs.text.splitlines()]
    rs = [i for i in rs if i != ""]
    return rs[0] + "の天気は" + rs[1] + "、明日の天気は" + rs[19] + "です。"

# Streamlitアプリの本体
def main():
    st.title("Yahoo天気予報取得アプリ")

    # CSVファイルからエリアコードを取得
    csv_path = "/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/天気用CSV/地域コード.csv"
    area_codes = get_area_codes(csv_path)

    # Streamlitのサイドバーにエリアコードの選択ボックスを追加
    selected_area_code = st.sidebar.selectbox("エリアコードを選択してください", area_codes)

    # エリアコードを使用して天気情報を取得
    weather_info = GetYahooWeather(selected_area_code)

    # 取得した天気情報を表示
    st.write(f"エリアコード {selected_area_code} の天気情報:")
    st.write(weather_info)

# Streamlitアプリの実行
if __name__ == "__main__":
    main()
