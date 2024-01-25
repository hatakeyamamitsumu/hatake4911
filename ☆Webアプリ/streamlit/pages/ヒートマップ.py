import streamlit as st
import pandas as pd
import numpy as np

def read_csv(uploaded_file, encoding=None):
    df = pd.read_csv(uploaded_file, encoding=encoding)
    return df

def colorize_column(df, col_idx):
    col_name = df.columns[col_idx]
    if pd.api.types.is_numeric_dtype(df[col_name]):
        max_val = df[col_name].max()
        min_val = df[col_name].min()
        color_values = np.arange(255, -5, -5)
        for i, color in enumerate(color_values):
            threshold = min_val + i * 5
            print(f"Processing column {col_name}, threshold: {threshold}")  # デバッグ用出力
            df.loc[df[col_name] >= threshold, col_name] = f'background-color: rgb({max(0, 255 - color)}, 0, 0)'
    return df


def process_dataframe(df):
    for col_idx in range(df.shape[1]):
        df = colorize_column(df, col_idx)
    return df.style

# ページのタイトル
st.title("CSVデータの数値列を着色表示")

# UTF-8用アップローダー
uploaded_file_utf8 = st.file_uploader("UTF-8エンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_utf8 is not None:
    st.subheader("UTF-8データフレーム")
    df_utf8 = read_csv(uploaded_file_utf8, encoding='utf-8')
    st.dataframe(process_dataframe(df_utf8))

# Shift-JIS用アップローダー
uploaded_file_shift_jis = st.file_uploader("Shift-JISエンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_shift_jis is not None:
    st.subheader("Shift-JISデータフレーム")
    df_shift_jis = read_csv(uploaded_file_shift_jis, encoding='shift-jis')
    st.dataframe(process_dataframe(df_shift_jis))

