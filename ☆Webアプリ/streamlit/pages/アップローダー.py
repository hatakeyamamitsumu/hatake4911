import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='csvファイル', layout='centered')

# CSVファイルのアップロードと読み込み
def load_csv_and_plot(file_uploader_key):
    uploaded_file = st.file_uploader('CSVファイル', type='csv', key=file_uploader_key)
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            st.markdown('#### DataFrame')
            st.dataframe(df)

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
            
        except Exception as e:
            st.error(f"エラー: {str(e)}")

# 2回呼び出しているので、関数を使ってコードの重複を削減
st.title('CSVファイルのアップロードと読み込み1')
load_csv_and_plot('csv1')

st.title('CSVファイルのアップロードと読み込み2')
load_csv_and_plot('csv2')
