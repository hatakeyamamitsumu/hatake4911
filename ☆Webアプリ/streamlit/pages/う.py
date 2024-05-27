import streamlit as st
import folium
from folium.plugins import MousePosition
from streamlit_folium import folium_static, st_folium

# サイドバーに緯度と経度の入力欄を作成
st.sidebar.header("緯度と経度の入力")
latitude_input = st.sidebar.text_input("緯度", key="latitude")
longitude_input = st.sidebar.text_input("経度", key="longitude")

# 初期値を設定
initial_lat = 35.0
initial_lon = 135.0
zoom_start = 10

# 地図を作成
m = folium.Map(location=[initial_lat, initial_lon], zoom_start=zoom_start)

# MousePositionプラグインを追加
MousePosition().add_to(m)

# フォリウムのクリックイベントを追加
click_event = folium.features.LatLngPopup()
m.add_child(click_event)

# Streamlitで地図を表示し、クリックイベントを取得
output = st_folium(m, width=700, height=500)

# クリックイベントから緯度経度を取得して転記
if output and 'last_clicked' in output:
    clicked_lat = output['last_clicked']['lat']
    clicked_lon = output['last_clicked']['lng']
    st.sidebar.text_input("緯度", value=str(clicked_lat), key="latitude", disabled=True)
    st.sidebar.text_input("経度", value=str(clicked_lon), key="longitude", disabled=True)

# 地図を表示
folium_static(m)
