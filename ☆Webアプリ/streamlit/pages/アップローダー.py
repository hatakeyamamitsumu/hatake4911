import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='csvファイル', layout='centered')

# CSVファイルのアップロードと読み込み
def load_csv_and_plot(file_uploader_key, encoding):
    uploaded_file = st.file_uploader('CSVファイル', type='csv', key=file_uploader_key)
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file, encoding=encoding)
            st.markdown('#### DataFrame')
            st.dataframe(df)

            # Create a multiselect dropdown for choosing columns
            selected_columns = st.multiselect("グラフ化したい列を選択してください。（取り込んだファイルがデータベース形式である場合に限られます）", df.columns)

            # 日ごとの選択された列を含む新しいデータフレームを作成
            df_selected_columns = df[selected_columns]

            # データを共有するための共通の軸を作成
            fig, ax1 = plt.subplots()

            # プロットを追加
            for i, column in enumerate(selected_columns):
                # 異なる色を使いたい場合、以下のように指定します
                color = plt.cm.viridis(i / len(selected_columns))  # カラーマップを利用して異なる色を生成
                ax1.set_xlabel('---')
                ax1.set_ylabel(column, color=color)
                ax1.plot(df.index, df_selected_columns[column], label=column, color=color)
                ax1.tick_params(axis='y', labelcolor=color)

            # グラフを表示
            ax1.legend(loc='upper left', bbox_to_anchor=(1, 1))
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"エラー: {str(e)}")

# UTF-8 の場合の処理
st.title('CSVファイルのアップロードと読み込み (UTF-8)')
load_csv_and_plot('csv_utf8', 'utf-8')

# Shift-JIS の場合の処理
st.title('CSVファイルのアップロードと読み込み (Shift-JIS)')
load_csv_and_plot('csv_shiftjis', 'shift-jis')
