import streamlit as st
import pandas as pd
from japanmap import picture

# CSVファイルの読み込み
data = pd.read_csv('/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/都道府県を塗り分け用ＣＳＶ/都道府県別の博物館の数.CSV', index_col=0)  # ファイルのパスを実際のデータに合わせて変更

# 最大の博物館の数を取得
max_museums = data['データ'].max()

# 都道府県ごとの色データを作成
color_data = {prefecture: (255, int(255 * (1 - museums / max_museums)), 0) for prefecture, museums in zip(data.index, data['博物館の数'])}

# Streamlitアプリの構築
st.title("都道府県ごとの博物館の数に基づく色付け")

# 日本地図を表示
st.image(picture(color_data), caption="日本地図", use_column_width=True)

# カラーバーを表示（博物館の数が多いほど赤くなる）
st.write("博物館の数に基づくカラーバー")
st.image([[255, 0, 0], [255, 255, 0], [0, 255, 0]], caption='Colorbar', use_column_width=False)

# グラフの詳細情報
st.write("都道府県ごとの博物館の数:")
st.write(data)

# データの統計情報
st.write("データの統計情報:")
st.write(data.describe())

# カラーバーの説明
st.write("カラーバーの説明:")
st.write("赤色が最大の博物館数を示し、黄色、緑色へと減少します。")

# Streamlitアプリを起動
st.show()
