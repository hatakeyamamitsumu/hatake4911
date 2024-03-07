import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.text("x軸を指定できるバージョン")

# CSVファイルのアップロードと読み込み
def load_csv_and_plot(file_uploader_key, encoding):
    uploaded_file = st.file_uploader('CSVファイル', type='csv', key=file_uploader_key)
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file, encoding=encoding)
            st.markdown('#### DataFrame')
            st.dataframe(df)

            # 列の選択
            selected_column = st.selectbox("X軸にしたい列を選択してください。(日本語非対応です)", df.columns, key="selected_column")

            # Create a multiselect dropdown for choosing columns
            selected_columns = st.multiselect("Y軸にしたい列を選択してください。（取り込んだファイルがデータベース形式である場合に限られます）", df.columns)

            # データを共有するための共通の軸を作成
            fig, ax1 = plt.subplots()

            # プロットを追加
            ax1.set_xlabel(selected_column)

            # Plot on the primary y-axis (ax1)
            for i, column in enumerate(selected_columns):
                color = plt.cm.viridis(i / len(selected_columns))
                ax1.plot(df[selected_column], df[column], label=column, color=color)
                ax1.tick_params(axis='y', labelcolor=color)

            # Create a secondary y-axis
            ax2 = ax1.twinx()

            # Plot on the secondary y-axis (ax2)
            for i, column in enumerate(selected_columns):
                color = plt.cm.viridis(i / len(selected_columns))
                ax2.plot(df[selected_column], df[column], label=column + " (Secondary Y)", linestyle='dashed', color=color)
                ax2.tick_params(axis='y', labelcolor=color)

            # Display legends
            ax1.legend(loc='upper left', bbox_to_anchor=(1, 1))
            ax2.legend(loc='upper left', bbox_to_anchor=(1, 0.9))

            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"エラー: {str(e)}")

# UTF-8 の場合の処理
st.title('CSVファイルのアップロードと読み込み (UTF-8)')
load_csv_and_plot('csv_utf8', 'utf-8')

# Shift-JIS の場合の処理
st.title('CSVファイルのアップロードと読み込み (Shift-JIS)')
load_csv_and_plot('csv_shiftjis', 'shift-jis')
