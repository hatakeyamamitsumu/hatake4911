import folium
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Googleドライブの認証情報
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json',
    scopes=['https://www.googleapis.com/auth/drive']
)

# 認証情報の読み込みと認証
gc = gspread.authorize(credentials)

# Googleドライブ内のCSVファイルのIDとURL
file_id = '1c6A5_rnoabBChQgqcw2RwVrI6jrepW3k'
file_url = f'https://drive.google.com/uc?id={file_id}'

# ユーザーから緯度と経度の入力を受け取る
latitude = st.number_input("緯度を入力してください", value=35.6895, step=0.0001)
longitude = st.number_input("経度を入力してください", value=139.6917, step=0.0001)

# 地図を作成
m = folium.Map(location=[latitude, longitude], zoom_start=10)

# 入力された緯度経度にピンを立てる
folium.Marker([latitude, longitude], popup='Selected Point').add_to(m)

# 地図を表示
folium_static(m)

# 書き込みボタンが押されたらデータを書き込む
if st.button("書き込み"):
    # ユーザーが書き込むデータを作成
    new_data = {'緯度': [latitude], '経度': [longitude]}

    # 新しいデータフレームを作成
    new_df = pd.DataFrame(new_data)

    # CSVファイルに新しいデータを追記
    existing_data = pd.read_csv(file_url)
    updated_data = pd.concat([existing_data, new_df], ignore_index=True)

    # GoogleドライブのCSVファイルに書き込む
    with open(file_url, 'w') as f:
        updated_data.to_csv(f, index=False)

    # ユーザーに成功メッセージを表示
    st.success("緯度経度がCSVファイルに書き込まれました。")
