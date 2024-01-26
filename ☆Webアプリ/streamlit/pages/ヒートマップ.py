import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def read_csv(uploaded_file, encoding=None):
    df = pd.read_csv(uploaded_file, encoding=encoding)
    return df

def heatmap_column(df, col_idx):
    col_name = df.columns[col_idx]
    if pd.api.types.is_numeric_dtype(df[col_name]):
        st.write(f"### {col_name} Heatmap")
        plt.figure(figsize=(10, 6))
        sns.heatmap(df[[col_name]].transpose(), cmap='Reds', annot=True, fmt=".2f", cbar_kws={'label': col_name})
        st.pyplot()

# ページのタイトル
st.title("CSVデータの数値列をヒートマップ表示")

# UTF-8のアップローダー
uploaded_file_utf8 = st.file_uploader("UTF-8エンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_utf8 is not None:
    df_utf8 = read_csv(uploaded_file_utf8, encoding='utf-8')

    # 見出し以外の数値列をヒートマップに
    for col_idx in range(1, df_utf8.shape[1]):  # 一番左の列を除外
        heatmap_column(df_utf8, col_idx)

# Shift-JISのアップローダー
uploaded_file_shift_jis = st.file_uploader("Shift-JISエンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_shift_jis is not None:
    df_shift_jis = read_csv(uploaded_file_shift_jis, encoding='shift-jis')

    # 見出し以外の数値列をヒートマップに
    for col_idx in range(1, df_shift_jis.shape[1]):  # 一番左の列を除外
        heatmap_column(df_shift_jis, col_idx)



