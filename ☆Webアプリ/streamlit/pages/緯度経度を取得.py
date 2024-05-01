import folium
import streamlit as st
import pandas as pd
from streamlit_folium import folium_static

# タイトルを設定
st.title("ピンを立てる")

# ユーザーから緯度と経度の入力を受け取る
latitude = st.number_input("緯度を入力してください", value=35.6895, step=0.0001)
longitude = st.number_input("経度を入力してください", value=139.6917, step=0.0001)

# 地図を作成
m = folium.Map(location=[latitude, longitude], zoom_start=10)

# 入力された緯度経度にピンを立てる
folium.Marker([latitude, longitude], popup='Selected Point').add_to(m)

# 地図を表示
folium_static(m)
