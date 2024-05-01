import folium
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Googleドライブの認証情報
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json',
    scopes=['https://www.googleapis.com/auth/drive']
)

# 認証情報の読み込みと認証
gc = gspread.authorize(credentials)

# Googleドライブ内のCSVファイルのID
file_id = '1c6A5_rnoabBChQgqcw2RwVrI6jrepW3k'

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
    try:
        # ユーザーが書き込むデータを作成
        new_data = {'緯度': [latitude], '経度': [longitude]}
        
        # 新しいデータフレームを作成
        new_df = pd.DataFrame(new_data)

        # GoogleドライブのCSVファイルを開く
        file = gc.open_by_key(file_id)
        worksheet = file.sheet1

        # 新しいデータをGoogle Sheetsに書き込む
        worksheet.append_row(new_df.values.tolist()[0])

        # ユーザーに成功メッセージを表示
        st.success("緯度経度がGoogle Sheetsに書き込まれました。")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
