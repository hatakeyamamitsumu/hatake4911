import folium
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import csv

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
    # CSVファイルへのパス
    file_path = '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.csv'
    
    # ユーザーが書き込むデータを作成
    new_data = {'緯度': [latitude], '経度': [longitude]}

    # 新しいデータフレームを作成
    new_df = pd.DataFrame(new_data)

    # 新しいデータをCSVファイルに追記
    with open(file_path, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(new_df.values[0].tolist())

    # ユーザーに成功メッセージを表示
    st.success("緯度経度がCSVファイルに書き込まれました。")
