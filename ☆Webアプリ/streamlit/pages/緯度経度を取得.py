import streamlit as st
import folium

# 地図を表示する領域を指定
map_center = [35.6895, 139.6917]  # 東京の緯度経度

# 地図を表示
m = folium.Map(location=map_center, zoom_start=12)

# 地図上のクリックしたポイントの緯度経度を格納するリスト
clicked_points = []

# 地図上のクリックを検知するコールバック関数
def handle_click(event, **kwargs):
    if event.originalEvent:
        lat, lon = event.latlng
        clicked_points.append((lat, lon))
        st.info(f"クリックしたポイントの緯度経度: 緯度 {lat}, 経度 {lon}")

# 地図にクリックイベントを追加
m.add_child(folium.ClickForMarker(popup=None, callback=handle_click))

# Streamlit で地図を表示
st.write(m)
