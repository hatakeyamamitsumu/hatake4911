import streamlit as st
import pandas as pd
import plotly.express as px

# CSVファイルの読み込み
data = pd.read_csv('都道府県別の博物館の数(2018).csv', index_col=0)

# 最大の博物館の数を取得
max_museums = data['データ'].max()

# 都道府県ごとの色データを作成
color_data = {prefecture: int(255 * (1 - museums / max_museums)) for prefecture, museums in zip(data.index, data['データ'])}

# グラフのサイズを設定
fig = px.choropleth(data, 
                    geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/japan.geojson",
                    featureidkey="properties.name",
                    locations=data.index,
                    color=color_data,
                    color_continuous_scale="reds",
                    title="都道府県ごとの博物館の数に基づく色付け",
                    labels={'color': '博物館の数'},
                    width=800, height=600)

# カラーバーを表示（博物館の数が多いほど赤くなる）
fig.update_layout(coloraxis_colorbar=dict(title='博物館の数'))

# Streamlit アプリの構築
st.title("都道府県ごとの博物館の数に基づく色付け")
st.plotly_chart(fig)
