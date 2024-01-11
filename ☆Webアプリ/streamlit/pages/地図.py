import folium
from streamlit_folium import folium_static
import streamlit as st
import pandas as pd

# ------------------------CSVファイル読み込み------------------------
file_path = "/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/町の緯度経度その他数値情報.csv"
sales_office = pd.read_csv(file_path, index_col=0)

# データを地図に渡す関数を作成する
def AreaMarker(df, m):
    for index, r in df.iterrows():

        # ピンをおく
        popup_content = f"<div style='font-size: 16px; width: 400px;'>{index}: {r.情報.replace(',', '<br>')}"

        # URLが含まれている場合はハイパーリンクを追加
        if 'https://' in r.情報:
            popup_content += f'<br><a href="{r.情報}" target="_blank">詳細を見る</a></div>'
        else:
            popup_content += '</div>'

        marker = folium.Marker(
            location=[r.緯度, r.経度],
            popup=folium.Popup(popup_content, parse_html=True),
        ).add_to(m)
        
        # 円を重ねる
        folium.Circle(
            radius=rad * 1000,
            location=[r.緯度, r.経度],
            popup=folium.Popup(f"{index}: {r.情報}", parse_html=True),  # ポップアップに情報列を表示
            color="yellow",
            fill=True,
            fill_opacity=0.07
        ).add_to(m)

# ------------------------画面作成------------------------

st.title("サンプル地図")  # タイトル

rad = st.slider('拠点を中心とした円の半径（km）',
                value=40, min_value=5, max_value=50)  # スライダーをつける
st.subheader("各拠点からの距離{:,}km".format(rad))  # 半径の距離を表示
m = folium.Map(location=[33.1, 131.0], zoom_start=7)  # 地図の初期設定
AreaMarker(sales_office, m)  # データを地図に渡す
folium_static(m)  # 地図情報を表示



