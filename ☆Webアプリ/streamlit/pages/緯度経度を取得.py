import streamlit as st

# 地図を表示
st.title('クリックしたポイントの緯度経度を取得する')
center = [35.6895, 139.6917]  # 東京の緯度経度
map_data = st.map(center=center, zoom=12)

# クリックしたポイントの緯度経度を表示
clicked_points = []

if map_data:
    clicked_points.append((map_data["lat"], map_data["lon"]))
    st.info(f"クリックしたポイントの緯度経度: 緯度 {map_data['lat']}, 経度 {map_data['lon']}")
