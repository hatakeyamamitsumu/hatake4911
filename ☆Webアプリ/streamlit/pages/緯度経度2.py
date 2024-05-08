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
st.title("情報とピンを立てる")

# 緯度の入力方法を選択
latitude_input = st.number_input("緯度を入力してください", min_value=-90.0, max_value=90.0, value=35.6895, step=0.0001)

# 経度の入力方法を選択
longitude_input = st.number_input("経度を入力してください", min_value=-180.0, max_value=180.0, value=139.6917, step=0.0001)

# 緯度と経度の入力が変更された時に、対応するスライダーの値も更新する
if "latitude_slider" not in st.session_state:
    st.session_state.latitude_slider = latitude_input
if "longitude_slider" not in st.session_state:
    st.session_state.longitude_slider = longitude_input

if st.session_state.latitude_input != latitude_input:
    st.session_state.latitude_slider = latitude_input
if st.session_state.longitude_input != longitude_input:
    st.session_state.longitude_slider = longitude_input

# スライダーを使って緯度と経度を選択
latitude_slider = st.slider("緯度を選択してください", min_value=-90.0, max_value=90.0, value=st.session_state.latitude_slider, step=0.0001)
longitude_slider = st.slider("経度を選択してください", min_value=-180.0, max_value=180.0, value=st.session_state.longitude_slider, step=0.0001)

# 入力値を更新
st.session_state.latitude_input = latitude_slider
st.session_state.longitude_input = longitude_slider

# ユーザーから情報の入力を受け取る
info = st.text_input("情報を入力してください")

# 地図を作成
m = folium.Map(location=[latitude_input, longitude_input], zoom_start=10)

# 入力された緯度経度にピンを立てる
folium.Marker([latitude_input, longitude_input], popup=info).add_to(m)

# 地図を表示
folium_static(m)

# 書き込みボタンを追加
if st.button("書き込み"):
    # Google Sheetsのデータを取得
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1X1mppebuIXGIGd-n_9pL6wHahk1-rFbO2tAjgc9mEqg/edit?usp=drive_link"
    sheet = client.open_by_url(spreadsheet_url).sheet1

    # 新しいデータをGoogle Sheetsに書き込む
    new_row = [latitude_input, longitude_input, info]
    sheet.append_row(new_row)

    # ユーザーに成功メッセージを表示
    st.success("情報と緯度経度がGoogle Sheetsに書き込まれました。")
