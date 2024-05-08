import streamlit as st
import folium
from streamlit_folium import st_folium

# 地図を作成
m = folium.Map(location=[35.6895, 139.6917], zoom_start=6)

# クリックイベントを設定
def click_event(click_location):
  folium.CircleMarker(click_location, radius=5, color='red').add_to(m)

m.on_click(click_event)

# 地図をStreamlitに表示
st_folium(m)
