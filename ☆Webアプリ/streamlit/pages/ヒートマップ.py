import streamlit as st
import pandas as pd
import numpy as np

def read_csv(uploaded_file, encoding=None):
    df = pd.read_csv(uploaded_file, encoding=encoding)
    return df

def colorize_max_value(df, col_idx):
    col_name = df.columns[col_idx]
    if pd.api.types.is_numeric_dtype(df[col_name]):
        max_value = df[col_name].max()
        st.write(f"### {col_name} - Max Value: {max_value}")
        max_idx = df[col_name].idxmax()
        st.dataframe(df.style.apply(lambda x: ['background: red' if i == max_idx else '' for i in range(len(x))], subset=col_name))

# ページのタイトル
st.title("CSVデータの数値列で最大値を赤く塗る")

# UTF-8のアップローダー
uploaded_file_utf8 = st.file_uploader("UTF-8エンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_utf8 is not None:
    df_utf8 = read_csv(uploaded_file_utf8, encoding='utf-8')

    # 見出し以外の数値列で最大値を赤く塗る
    for col_idx in range(1, df_utf8.shape[1]):  # 一番左の列を除外
        colorize_max_value(df_utf8, col_idx)

# Shift-JISのアップローダー
uploaded_file_shift_jis = st.file_uploader("Shift-JISエンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_shift_jis is not None:
    df_shift_jis = read_csv(uploaded_file_shift_jis, encoding='shift-jis')

    # 見出し以外の数値列で最大値を赤く塗る
    for col_idx in range(1, df_shift_jis.shape[1]):  # 一番左の列を除外
        colorize_max_value(df_shift_jis, col_idx)




