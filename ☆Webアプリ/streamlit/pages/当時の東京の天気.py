import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.write("２０２２年１０月の東京の天気（気象庁より取得.降雨、積雪の欠損値を0としております）")
st.write("https://www.data.jma.go.jp/stats/etrn/index.php")  
df = pd.read_csv("/mount/src/hatake4911/☆Webアプリ/csvファイル各種/２０２２年１０月の東京の天気.csv", encoding='shift_jis',index_col="日")
st.dataframe(df, height=250)

# 日ごとの平均気温と降水量を含む新しいデータフレームを作成
df_plot_temp = df[['平均気温(℃)']]
df_plot_rain = df[['降水量(mm)合計']]

# Streamlitで折れ線グラフと縦棒グラフを描画
#st.title("気温")
#st.line_chart(df_plot_temp,y='平均気温(℃)',use_container_width=True,height=250)
#st.title("降水量")
#st.bar_chart(df_plot_rain,y="降水量(mm)合計" ,use_container_width=True, height=250)




# データを共有するための共通の軸を作成
fig, ax1 = plt.subplots()

# 1つ目の軸（気温）をプロット
st.title("気温と降水量")
color = 'tab:red'
ax1.set_xlabel('day')
ax1.set_ylabel('temperature(℃)', color=color)
ax1.plot(df_plot_temp.index, df_plot_temp['平均気温(℃)'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

# 2つ目の軸（降水量）をプロット
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('total_rain(mm)', color=color)
ax2.bar(df_plot_rain.index, df_plot_rain['降水量(mm)合計'], color=color, alpha=0.5)
ax2.tick_params(axis='y', labelcolor=color)

# グラフを表示
st.pyplot(fig)





# Create a multiselect dropdown for choosing columns
selected_columns = st.multiselect("Select Columns for Plotting", df.columns)

# 日ごとの選択された列を含む新しいデータフレームを作成
df_selected_columns = df[selected_columns]

# データを共有するための共通の軸を作成
fig, ax1 = plt.subplots()

# プロットを追加
for column in selected_columns:
    color = 'tab:red'  # You can choose different colors for each line
    ax1.set_xlabel('day')
    ax1.set_ylabel(column, color=color)
    ax1.plot(df.index, df_selected_columns[column], color=color, label=column)
    ax1.tick_params(axis='y', labelcolor=color)

# グラフを表示
ax1.legend(loc='upper left', bbox_to_anchor=(1, 1))
st.pyplot(fig)
