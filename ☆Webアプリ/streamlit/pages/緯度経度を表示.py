import folium
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_folium import folium_static

# Google Sheetsの認証情報
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json", scope)  
client = gspread.authorize(creds)

# タイトルを設定
st.title("スプレッドシートから地図上に表示")

# スプレッドシートからデータを取得
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1X1mppebuIXGIGd-n_9pL6wHahk1-rFbO2tAjgc9mEqg/edit?usp=drive_link"
sheet = client.open_by_url(spreadsheet_url).sheet1
data = sheet.get_all_values()

# 地図を作成
m = folium.Map()

# データから緯度経度を取得し、ピンを立てる
for row in data[1:]:  # ヘッダーを除く
    latitude, longitude, info = float(row[0]), float(row[1]), row[2]
    folium.Marker([latitude, longitude], popup=info).add_to(m)

# 地図を表示
folium_static(m)

