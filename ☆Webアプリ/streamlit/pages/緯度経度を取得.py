import streamlit as st
from folium import Map

# 地図を表示
st.title('クリックしたポイントの緯度経度を取得する')
center = [35.6895, 139.6917]  # 東京の緯度経度
m = Map(center=center, zoom=12)

# クリックイベントを設定
def on_click(event):
    latitude = event.lat
    longitude = event.lng
    st.info(f"クリックしたポイントの緯度経度: 緯度 {latitude}, 経度 {longitude}")

m.on_click = on_click

# 地図をStreamlitに表示
st_folium(m)
