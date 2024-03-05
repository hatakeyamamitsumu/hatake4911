import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='CSVファイル', layout='centered')

# CSVファイルのアップロードと読み込み
def load_csv_and_plot(file_uploader_key, encoding):
    uploaded_file = st.file_uploader('CSVファイル', type='csv', key=file_uploader_key)
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file, encoding=encoding)
            st.markdown('#### DataFrame')
            st.dataframe(df)

            # 日時の列がある場合は、その列を x 軸に使う
            date_column = st.selectbox("日時の列を選択してください。", df.columns, key="date_column")

            # 日時列が存在する場合、日時をインデックスに設定
            if date_column in df.columns:
                df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
                df.set_index(date_column, inplace=True)

            # グラフの種類を選択
            chart_type = st.selectbox("グラフの種類を選択してください。", ["折れ線グラフ", "棒グラフ", "散布図"])

            # 選択された列をグラフ化
            if chart_type == "折れ線グラフ":
                st.line_chart(df)
            elif chart_type == "棒グラフ":
                st.bar_chart(df)
            elif chart_type == "散布図":
                selected_columns = st.multiselect("X軸とY軸を選択してください。", df.columns)
                if len(selected_columns) == 2:
                    st.scatter_chart(df, x=selected_columns[0], y=selected_columns[1])
                else:
                    st.warning("2つの列を選択してください。")

        except Exception as e:
            st.error(f"エラー: {str(e)}")

# UTF-8 の場合の処理
st.title('CSVファイルのアップロードと読み込み (UTF-8)')
load_csv_and_plot('csv_utf8', 'utf-8')

# Shift-JIS の場合の処理
st.title('CSVファイルのアップロードと読み込み (Shift-JIS)')
load_csv_and_plot('csv_shiftjis', 'shift-jis')
