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
selected_file = st.selectbox("Select CSV file", csv_files)

# Check if a file was selected
if selected_file:
    # Construct the full file path
    file_path = os.path.join(folder_path, selected_file)
    
    # Read the selected CSV file
    sales_office = pd.read_csv(file_path)
else:
    st.warning("Please select a CSV file.")

# データを地図に渡す関数を作成する
def AreaMarker(df, m):
    for index, r in df.iterrows():
        # ピンをおく
        folium.Marker(
            location=[r.緯度, r.経度],
            popup=f"<div style='font-size: 16px; width: 800px;'>{index}: {r.情報}</div>",
        ).add_to(m)
        
        # 円を重ねる
        folium.Circle(
            radius=rad * 1000,
            location=[r.緯度, r.経度],
            color="yellow",
            fill=True,
            fill_opacity=0.07
        ).add_to(m)

        # 縦棒グラフを表示する
        folium.Marker(
            location=[r.緯度, r.経度],
            icon=folium.Icon(color='blue', icon='bar-chart', prefix='fa'),
            popup=f"<div style='font-size: 16px; width: 800px;'>{index}: {r.情報}</div>",
        ).add_to(m)

# ------------------------画面作成------------------------

st.title("サンプル地図")  # タイトル

# Check if a CSV file was selected
if selected_file is not None:
    st.subheader("各拠点からの距離 - CSVファイル: {}".format(selected_file))
    m = folium.Map(location=[33.1, 131.0], zoom_start=7)  # 地図の初期設定
    rad = st.slider('拠点を中心とした円の半径（km）',
                    value=40, min_value=1, max_value=50)  # スライダーをつける
    AreaMarker(sales_office, m)  # データを地図に渡す
    folium_static(m)  # 地図情報を表示
else:
    st.warning("Please select a CSV file.")
