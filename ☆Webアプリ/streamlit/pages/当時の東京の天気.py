import streamlit as st
import pandas as pd
st.write("２０２２年１０月の東京の天気（気象庁より取得）")
st.write("https://www.data.jma.go.jp/stats/etrn/index.php")  
df = pd.read_csv("/mount/src/hatake4911/☆Webアプリ/csvファイル各種/２０２２年１０月の東京の天気.csv", encoding='shift_jis',index_col="日")
st.dataframe(df)

# CSVファイルからデータを読み込む
df = pd.read_csv("/mount/src/hatake4911/☆Webアプリ/csvファイル各種/２０２２年１０月の東京の天気.csv",encoding='shift_jis')

# 日ごとの平均気温と降水量を含む新しいデータフレームを作成
df_plot = df[['日', '平均気温(℃)', '降水量(mm)合計']]

# 日をインデックスに設定
df_plot.set_index('日', inplace=True)

# Streamlitで折れ線グラフを描画
st.line_chart(df_plot)
