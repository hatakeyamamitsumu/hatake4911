import streamlit as st
from streamlit_folium import st_folium
import folium

# 初期値
initial_latitude = 35.6895  # 東京駅の緯度
initial_longitude = 139.6917  # 東京駅の経度

# スライダーの設定
latitude_slider = st.slider('緯度', 30, 45, initial_value=initial_latitude)
longitude_slider = st.slider('経度', 130, 145, initial_value=initial_longitude)

# 地図を作成
m = folium.Map(location=[initial_latitude, initial_longitude], zoom_start=7)

# マーカーを作成
folium.CircleMarker([initial_latitude, initial_longitude], radius=5, color='red').add_to(m)

# スライダーの値が変更されたら、地図とマーカーを更新
def update_map():
    new_latitude = latitude_slider
    new_longitude = longitude_slider

    m.location = [new_latitude, new_longitude]
    m.clear()
    folium.CircleMarker([new_latitude, new_longitude], radius=5, color='red').add_to(m)

# 地図をStreamlitに表示
st_folium(m)

# ボタンを作成
update_button = st.button('更新')

# ボタンがクリックされたら、地図とマーカーを更新
if update_button:
    update_map()
