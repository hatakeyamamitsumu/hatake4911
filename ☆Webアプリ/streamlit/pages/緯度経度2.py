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
st.title("地図にピンを立てる")
# 地図の拡大率の設定
zoom_value = st.slider("地図の拡大率を固定できます", min_value=1, max_value=20, value=10)
# 緯度の入力方法を選択
latitude_slider = st.sidebar.slider("緯度を選択してください", min_value=-90.000000, max_value=90.000000, value=35.689500, step=0.000001)
latitude_input = st.sidebar.number_input("緯度を入力してください", value=latitude_slider, step=0.000001, format="%.6f", key="latitude")

# 経度の入力方法を選択
longitude_slider = st.sidebar.slider("経度を選択してください", min_value=-180.000000, max_value=180.000000, value=139.691700, step=0.000001)
longitude_input = st.sidebar.number_input("経度を入力してください", value=longitude_slider, step=0.000001, format="%.6f", key="longitude")

# ユーザーから情報の入力を受け取る
info = st.sidebar.text_input("情報を入力してください")



# 地図を作成
m = folium.Map(location=[latitude_input, longitude_input], zoom_start=zoom_value)

# 入力された緯度経度にピンを立てる
folium.Marker([latitude_input, longitude_input], popup=info).add_to(m)

# 地図を表示
folium_static(m)

# 書き込みボタンを追加
if st.sidebar.button("書き込み"):
    # Google Sheetsのデータを取得
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1X1mppebuIXGIGd-n_9pL6wHahk1-rFbO2tAjgc9mEqg/edit?usp=drive_link"
    sheet = client.open_by_url(spreadsheet_url).sheet1

    # 新しいデータをGoogle Sheetsに書き込む
    new_row = [latitude_input, longitude_input, info]
    sheet.append_row(new_row)

    # ユーザーに成功メッセージを表示
    st.sidebar.success("情報と緯度経度がGoogle Sheetsに書き込まれました。")
