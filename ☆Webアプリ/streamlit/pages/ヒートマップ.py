import streamlit as st
from streamlit_folium import folium_static
import folium
from folium import plugins

# 中心座標(適当)
center = [32, 131]

# ベースの地図作成
m = folium.Map(center, zoom_start=12)

# ヒートマップ層を地図に追加
folium.plugins.HeatMap(
    data=[center]  # 注意！ ２次元にして渡す
).add_to(m)

# Streamlit で地図を表示
st.header("ヒートマップの例")
folium_static(m)

