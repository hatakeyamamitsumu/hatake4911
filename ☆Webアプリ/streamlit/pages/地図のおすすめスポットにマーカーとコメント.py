import folium
from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import os

# ------------------------CSVファイル読み込み------------------------

# Specify the folder path
folder_path = "/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/地図用CSV"

# List all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Allow the user to select a CSV file
selected_file = st.selectbox("リストを選んでください", csv_files)

# Check if a file was selected
if selected_file:
    # Construct the full file path
    file_path = os.path.join(folder_path, selected_file)
    
    # Read the selected CSV file
    sales_office = pd.read_csv(file_path, index_col=0)
else:
    st.warning("Please select a CSV file.")

# データを地図に渡す関数を作成する
def AreaMarker(df, m):
    for index, r in df.iterrows():

        # ピンをおく
        marker = folium.Marker(
            location=[r.緯度, r.経度],
            popup=f"<div style='font-size: 16px; width: 800px;'>{index}: {r.情報.replace(',', '<br>')}</div>",
            icon=folium.Icon(color='red')  # ピンの色を赤に設定
        ).add_to(m)
        
        # 円を重ねる
        folium.Circle(
            radius=rad * 1000,
            location=[r.緯度, r.経度],
            color="yellow",
            fill=True,
            fill_opacity=0.07
        ).add_to(m)

# ------------------------画面作成------------------------

st.title("Hatの独断おすすめスポット（マーカー+コメント）")  # タイトル

rad = st.slider('スポットを中心とした円の半径（km）',
                value=5, min_value=1, max_value=50)  # スライダーをつける

# Check if a CSV file was selected
if selected_file is not None:
    st.subheader("各スポットからの距離{}km - CSVファイル: {}".format(rad, selected_file))  # 半径の距離を表示
    m = folium.Map(location=[33.1, 131.0], zoom_start=7)  # 地図の初期設定
    AreaMarker(sales_office, m)  # データを地図に渡す
    folium_static(m)  # 地図情報を表示
else:
    st.warning("Please select a CSV file.")
