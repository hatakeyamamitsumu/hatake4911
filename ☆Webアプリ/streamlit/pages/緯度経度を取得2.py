import folium
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_folium import folium_static



# Google Sheetsの認証情報
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json', scope)
client = gspread.authorize(creds)

# Google Sheetsのデータを取得
sheet = client.open("Your Google Sheets File Name").sheet1

# タイトルを設定
st.title("ピンを立てる")

# ユーザーから緯度と経度の入力を受け取る
latitude = st.number_input("緯度を入力してください", value=35.6895, step=0.0001)
longitude = st.number_input("経度を入力してください", value=139.6917, step=0.0001)

# 地図を作成
m = folium.Map(location=[latitude, longitude], zoom_start=10)

# 入力された緯度経度にピンを立てる
folium.Marker([latitude, longitude], popup='Selected Point').add_to(m)

# 地図を表示
folium_static(m)

# 新しいデータをGoogle Sheetsに書き込む
new_data = {'緯度': latitude, '経度': longitude}
sheet.append_row([new_data['緯度'], new_data['経度']])

# ユーザーに成功メッセージを表示
st.success("緯度経度がGoogle Sheetsに書き込まれました。")
