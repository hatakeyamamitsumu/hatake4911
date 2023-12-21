import streamlit as st
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt

st.set_page_config(page_title='csvファイル',layout='centered')
st.title('CSVファイルのアップロードと読み込み1')
uploaded_file=st.file_uploader('utf-8 CSV',type='csv',key='csv1')#keyはアップローダーが複数あった時にそれぞれにつけるラベルのようなもの

if uploaded_file:
  df1=pd.read_csv(uploaded_file,encoding='utf-8')
  st.markdown('#### dataframe')
  st.dataframe(df1)

# Create a multiselect dropdown for choosing columns
selected_columns = st.multiselect("Select Columns for Plotting", df.columns)

# 日ごとの選択された列を含む新しいデータフレームを作成
df_selected_columns = df1[selected_columns]

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





st.title('CSVファイルのアップロードと読み込み2')
uploaded_file=st.file_uploader('shift-jis CSV',type='csv',key='csv2')#keyはアップローダーが複数あった時にそれぞれにつけるラベルのようなもの

if uploaded_file:
  df2=pd.read_csv(uploaded_file,encoding='shift-jis')
  st.markdown('#### dataframe')
  st.dataframe(df2)

# Create a multiselect dropdown for choosing columns
selected_columns = st.multiselect("Select Columns for Plotting", df.columns)

# 日ごとの選択された列を含む新しいデータフレームを作成
df_selected_columns = df2[selected_columns]

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
