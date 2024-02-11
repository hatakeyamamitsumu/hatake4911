import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# CSVファイルの読み込み
data = pd.read_csv('/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/都道府県を塗り分け用ＣＳＶ/都道府県別の博物館の数.CSV', index_col=0)

# GeoJSON ファイルの読み込み
geojson_url = 'https://raw.githubusercontent.com/niiyz/Japan-Geojson/master/geojson/prefectures.geojson'
geojson_gdf = gpd.read_file(geojson_url)

# データの結合
merged_gdf = geojson_gdf.merge(data, left_on='name', right_index=True)

# 描画
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
merged_gdf.plot(column='データ', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

# カラーバーを追加
cax = fig.add_axes([0.9, 0.5, 0.03, 0.3])
sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=data['データ'].min(), vmax=data['データ'].max()))
sm._A = []
fig.colorbar(sm, cax=cax, label='博物館の数')

# タイトルとラベル
plt.title('都道府県ごとの博物館の数')
plt.xlabel('経度')
plt.ylabel('緯度')

# Streamlit アプリの構築
st.title("都道府県ごとの博物館の数に基づく色付け")
st.pyplot(fig)

