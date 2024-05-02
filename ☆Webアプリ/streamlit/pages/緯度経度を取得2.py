import folium
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_folium import folium_static

# Google Sheetsの認証情報
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("your_credentials.json", scope)  # "your_credentials.json" を実際のJSONキーファイルへのパスに置き換えてください
client = gspread.authorize(creds)

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

# 書き込みボタンを追加
if st.button("書き込み"):
    # Google Sheetsのデータを取得
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1X1mppebuIXGIGd-n_9pL6wHahk1-rFbO2tAjgc9mEqg/edit?usp=drive_link"
    sheet = client.open_by_url(spreadsheet_url).sheet1

    # 新しいデータをGoogle Sheetsに書き込む
    new_row = [latitude, longitude]
    sheet.append_row(new_row)

    # ユーザーに成功メッセージを表示
    st.success("緯度経度がGoogle Sheetsに書き込まれました。")
