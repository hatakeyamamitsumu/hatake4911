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
    num_rows, num_cols = df.shape

    for i in range(1, 26):
        if i == 25:
            break

        color = f'rgb({255 - i * 10}, 0, 0)'
        for col_idx in range(num_cols):
            rank_series = df.iloc[:, col_idx].rank(ascending=False, method='min')
            styled_df.iloc[:, col_idx] = np.where(rank_series == i, f'background-color: {color}', styled_df.iloc[:, col_idx])

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
