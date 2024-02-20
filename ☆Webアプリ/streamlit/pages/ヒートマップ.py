import folium
import pandas as pd
import streamlit as st

# データの準備
df = pd.read_csv("緯度,経度
35.652832,139.839478
35.658581,139.840439
35.660333,139.836389")

# サイドバーで半径の値を選択できるようにする
radius = st.sidebar.slider('熱マップの半径', 10, 50, 15)

# 地図の作成
map = folium.Map(location=[35.652832, 139.839478], zoom_start=10)

# 熱マップの生成
heatmap = folium.HeatMap(data=df[['緯度', '経度']], radius=radius).add_to(map)

# 地図の表示
folium_static(map)
