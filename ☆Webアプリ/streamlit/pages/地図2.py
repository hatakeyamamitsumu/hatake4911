import streamlit as st
import pandas as pd
import folium

# CSVファイルを読み込む
file_path = "/mount/src/hatake4911/☆Webアプリ/動画/東京到着.gif'  # ファイルのパスを適切に指定してください
data = pd.read_csv(file_path)

# Streamlitアプリのタイトル
st.title("緯度経度位置に縦棒グラフを表示するアプリ")

# 地図の初期表示位置を設定
map_center = [data["緯度"].mean(), data["経度"].mean()]

# Foliumマップを作成
my_map = folium.Map(location=map_center, zoom_start=12)

# データを地図上に表示
for index, row in data.iterrows():
    folium.Marker(
        location=[row["緯度"], row["経度"]],
        popup=row["情報"]
    ).add_to(my_map)

# Streamlitで地図を表示
st.write(my_map)

# 縦棒グラフを表示
st.bar_chart(data.set_index("都道府県名")["情報"])

