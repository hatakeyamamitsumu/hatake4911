import streamlit as st
import pandas as pd
import numpy as np

def read_csv(uploaded_file, encoding):
    df = pd.read_csv(uploaded_file, encoding=encoding)
    return df

# ページのタイトル
st.title("CSVデータベースのセルを着色で強調表示")

# ファイルアップローダー
uploaded_file_utf8 = st.file_uploader("UTF-8エンコーディングのCSVファイルをアップロードしてください", type=["csv"])
uploaded_file_shift_jis = st.file_uploader("Shift-JISエンコーディングのCSVファイルをアップロードしてください", type=["csv"])

def highlight_cells(df):
    styled_df = df.copy()
    num_cols = len(df.columns)

    for i in range(1, 26):
        color = (255 - i * 10, 0, 0)
        styled_df.iloc[:, i - 1] = styled_df.iloc[:, i - 1].apply(lambda x: f'background-color: rgb{color}' if x == x else '')

    return styled_df

# UTF-8データベースの処理
if uploaded_file_utf8 is not None:
    st.subheader("UTF-8データベース")
    df_utf8 = read_csv(uploaded_file_utf8, 'utf-8')
    st.dataframe(highlight_cells(df_utf8))

# Shift-JISデータベースの処理
if uploaded_file_shift_jis is not None:
    st.subheader("Shift-JISデータベース")
    df_shift_jis = read_csv(uploaded_file_shift_jis, 'shift-jis')
    st.dataframe(highlight_cells(df_shift_jis))





