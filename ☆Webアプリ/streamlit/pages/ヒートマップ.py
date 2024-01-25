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

# UTF-8のアップローダー
uploaded_file_utf8 = st.file_uploader("UTF-8エンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_utf8 is not None:
    df_utf8 = read_csv(uploaded_file_utf8, encoding='utf-8')

    # 列ごとに処理
    for col_idx in range(1, df_utf8.shape[1]):  # 一番左の列を除外
        try:
            df_utf8 = colorize_column(df_utf8, col_idx)
        except KeyError as e:
            st.error(f"Error processing column {df_utf8.columns[col_idx]}: {e}")
            break

    # 表示
    st.dataframe(df_utf8)

# Shift-JISのアップローダー
uploaded_file_shift_jis = st.file_uploader("Shift-JISエンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_shift_jis is not None:
    df_shift_jis = read_csv(uploaded_file_shift_jis, encoding='shift-jis')

    # 列ごとに処理
    for col_idx in range(1, df_shift_jis.shape[1]):  # 一番左の列を除外
        try:
            df_shift_jis = colorize_column(df_shift_jis, col_idx)
        except KeyError as e:
            st.error(f"Error processing column {df_shift_jis.columns[col_idx]}: {e}")
            break

    # 表示
    st.dataframe(df_shift_jis)



