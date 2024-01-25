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
            try:
                df.loc[df[col_name] >= threshold, col_name] = f'background-color: rgb({max(0, 255 - color)}, 0, 0)'
            except Exception as e:
                st.error(f"Error processing column {col_name}: {e}")
                return df
    return df

# ページのタイトル
st.title("CSVデータの数値列を着色表示")

# 1つ目のアップローダー
uploaded_file_1 = st.file_uploader("1つ目のCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_1 is not None:
    df_1 = read_csv(uploaded_file_1)

    # 列ごとに処理
    for col_idx in range(1, df_1.shape[1]):  # 一番左の列を除外
        df_1 = colorize_column(df_1, col_idx)

    # 表示
    st.dataframe(df_1)

# 2つ目のアップローダー
uploaded_file_2 = st.file_uploader("2つ目のCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_2 is not None:
    df_2 = read_csv(uploaded_file_2)

    # 列ごとに処理
    for col_idx in range(1, df_2.shape[1]):  # 一番左の列を除外
        df_2 = colorize_column(df_2, col_idx)

    # 表示
    st.dataframe(df_2)


