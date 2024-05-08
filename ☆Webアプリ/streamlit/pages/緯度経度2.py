import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# データの読み込み
df = pd.DataFrame({
    'lat': [35.681236, 35.681236, 37.7749],
    'lon': [139.767125, 139.767125, -122.4194],
    'name': ['東京タワー', '東京駅', 'サンフランシスコ']
})

# 地図の初期化
st.write("地図上でクリックしてピンを立てることができます")
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=5)

# ピンを立てる
for i, row in df.iterrows():
    folium.Marker([row['lat'], row['lon']], popup=row['name']).add_to(m)

# 地図を表示
folium_static(m)
