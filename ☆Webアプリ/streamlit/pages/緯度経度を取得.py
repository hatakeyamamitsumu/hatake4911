import streamlit as st
import folium

# Streamlitアプリケーションのタイトルを設定
st.title('地図上にピンを立てる')

# ユーザーからの緯度経度の入力を受け取る
latitude = st.number_input("緯度を入力してください", value=35.6895, step=0.0001)
longitude = st.number_input("経度を入力してください", value=139.6917, step=0.0001)

# 地図を表示する領域を指定
map_center = [latitude, longitude]

# 地図を作成
m = folium.Map(location=map_center, zoom_start=12)

# 入力された緯度経度にピンを立てる
folium.Marker(location=[latitude, longitude], popup='Selected Point').add_to(m)

# Streamlitで地図を表示
folium_static(m)
