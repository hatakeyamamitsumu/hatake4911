import streamlit as st
from streamlit_folium import st_folium
import folium

# 地図の中心座標とズームレベルを設定
center = [35.6895, 139.6917]  # 東京駅の緯度経度
zoom_start = 7

# Streamlitアプリの設定
st.set_page_config(layout="wide")

# 地図を作成
m = folium.Map(location=center, zoom_start=zoom_start)

# クリックイベントを設定
def on_click(event):
    latitude = event.lat
    longitude = event.lng
    print(f"緯度: {latitude}, 経度: {longitude}")

    # クリックした座標にマーカーを追加
    folium.CircleMarker([latitude, longitude], radius=5, color='red').add_to(m)

m.on_click = on_click

# Streamlitに地図を表示
st_folium(m)

# クリックされた緯度経度を表示
if 'latitude' in st.session_state:
    latitude = st.session_state['latitude']
    longitude = st.session_state['longitude']
    st.write(f"クリックされた緯度経度: 緯度: {latitude}, 経度: {longitude}")
