import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.write("２０２２年１０月の東京の天気（気象庁より取得）")
st.write("https://www.data.jma.go.jp/stats/etrn/index.php")  
df = pd.read_csv("/mount/src/hatake4911/☆Webアプリ/csvファイル各種/２０２２年１０月の東京の天気.csv", encoding='shift_jis',index_col="日")
st.dataframe(df, height=250)

# 日ごとの平均気温と降水量を含む新しいデータフレームを作成
df_plot_temp = df[['平均気温(℃)']]
df_plot_rain = df[['降水量(mm)合計']]

# Streamlitで折れ線グラフと縦棒グラフを描画
st.title("気温")
st.line_chart(df_plot_temp,y='平均気温(℃)',use_container_width=True,height=250)
st.title("降水量")
st.bar_chart(df_plot_rain,y="降水量(mm)合計" ,use_container_width=True, height=250)
