import streamlit as st
import requests
from bs4 import BeautifulSoup

def GetYahooWeather(AreaCode):
    """
    Yahoo天気予報をスクレイピングする関数。

    Parameters
    ----------
    AreaCode : str
        対象となる数値を指定。
    
    Returns
    -------
    str
    """
    url = "https://weather.yahoo.co.jp/weather/jp/13/" + str(AreaCode) + ".html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    rs = soup.find(class_='forecastCity')
    rs = [i.strip() for i in rs.text.splitlines()]
    rs = [i for i in rs if i != ""]
    return rs[0] + "の天気は" + rs[1] + "、明日の天気は" + rs[19] + "です。"

# Streamlitアプリの本体
def main():
    st.title("Yahoo天気予報取得アプリ")

    # Streamlitのサイドバーにエリアコードの入力フィールドを追加
    area_code = st.sidebar.text_input("エリアコードを入力してください", "4410")

    # エリアコードを使用して天気情報を取得
    weather_info = GetYahooWeather(area_code)

    # 取得した天気情報を表示
    st.write(f"エリアコード {area_code} の天気情報:")
    st.write(weather_info)

# Streamlitアプリの実行
if __name__ == "__main__":
    main()
