import streamlit as st
import pandas as pd

# データの読み込み
df = pd.DataFrame({
    'lat': [35.681236, 35.681236, 37.7749],
    'lon': [139.767125, 139.767125, -122.4194],
    'name': ['東京タワー', '東京駅', 'サンフランシスコ']
})

# 地図の初期化
st.write("地図上でクリックしてピンを立てることができます")
map_data = df[['lat', 'lon']]
st.map(map_data)

# ピンを立てる
if st.button("ピンを立てる"):
    new_marker_lat = st.number_input("緯度を入力してください:")
    new_marker_lon = st.number_input("経度を入力してください:")
    new_marker_name = st.text_input("マーカーの名前を入力してください:")
    if new_marker_lat and new_marker_lon and new_marker_name:
        st.write(f"新しいマーカー: ({new_marker_lat}, {new_marker_lon}, {new_marker_name})")
        new_marker = pd.DataFrame({'lat': [new_marker_lat], 'lon': [new_marker_lon], 'name': [new_marker_name]})
        df = pd.concat([df, new_marker], ignore_index=True)
        map_data = df[['lat', 'lon']]
        st.map(map_data)
