import streamlit as st
import pandas as pd
st.write("２０２２年１０月の東京の天気（気象庁より取得）")
st.write("https://www.data.jma.go.jp/stats/etrn/index.php")  
df = pd.read_csv("/mount/src/hatake4911/☆Webアプリ/csvファイル各種/２０２２年１０月の東京の天気.csv", encoding='shift_jis',index_col="日")
st.dataframe(df)

# 日ごとの平均気温と降水量を含む新しいデータフレームを作成
df_plot_temp = df[['平均気温(℃)']]
df_plot_rain = df[['降水量(mm)合計']]

# 降水量(mm)合計で降順にソート
df_plot_rain = df_plot_rain.sort_values(by='降水量(mm)合計', descending=True)

# Streamlitで折れ線グラフと縦棒グラフを描画
st.line_chart(df_plot_temp, use_container_width=True)

# 降水量(mm)合計の縦棒グラフを描画
st.bar_chart(df_plot_rain, use_container_width=True, height=400)
