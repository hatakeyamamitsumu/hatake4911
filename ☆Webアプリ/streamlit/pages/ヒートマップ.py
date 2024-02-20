import folium
import pandas as pd
import streamlit as st

# データの準備 main/☆Webアプリ/CSVファイル各種/ヒートマップ用CSV/ヒートマップ用緯度経度情報.csv
#/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/ヒートマップ用CSV/ヒートマップ用緯度経度情報.csv
df['緯度'] = df['緯度'].astype('float')
df['経度'] = df['経度'].astype('float')
# 緯度と経度の情報
latitudes = [35.652832, 35.658581, 35.660333]
longitudes = [139.839478, 139.840439, 139.836389]

# データの準備
df = pd.DataFrame({'緯度': latitudes, '経度': longitudes})

# サイドバーで半径の値を選択できるようにする
radius = st.sidebar.slider('熱マップの半径', 10, 50, 15)

# 地図の作成
map = folium.Map(location=[latitudes[0], longitudes[0]], zoom_start=10)

# 熱マップの生成
heatmap = folium.HeatMap(data=df[['緯度', '経度']], radius=radius).add_to(map)

# 地図の表示
folium_static(map)
