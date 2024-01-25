import streamlit as st
import pandas as pd

def read_csv(uploaded_file, encoding=None):
    df = pd.read_csv(uploaded_file, encoding=encoding)
    return df

def colorize_column(df, col_idx, color_values):
    col_name = df.columns[col_idx]
    if pd.api.types.is_numeric_dtype(df[col_name]):
        rank_col = df[col_name].rank(method='first', ascending=False) * 5
        for i, color in enumerate(color_values):
            df[rank_col <= i] = df.style.applymap(lambda x: f'background-color: rgb({max(0, 255 - color)}, 0, 0)', subset=pd.IndexSlice[:, col_name])
    return df

# ページのタイトル
st.title("CSVデータの数値列を着色表示")

# UTF-8用アップローダー
uploaded_file_utf8 = st.file_uploader("UTF-8エンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_utf8 is not None:
    st.subheader("UTF-8データフレーム")
    df_utf8 = read_csv(uploaded_file_utf8, encoding='utf-8')

    # 列ごとに処理
    for col_idx in range(df_utf8.shape[1]):
        color_values = range(255, -1, -5)
        df_utf8 = colorize_column(df_utf8, col_idx, color_values)

    # 表示
    st.dataframe(df_utf8)

# Shift-JIS用アップローダー
uploaded_file_shift_jis = st.file_uploader("Shift-JISエンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_shift_jis is not None:
    st.subheader("Shift-JISデータフレーム")
    df_shift_jis = read_csv(uploaded_file_shift_jis, encoding='shift-jis')

    # 列ごとに処理
    for col_idx in range(df_shift_jis.shape[1]):
        color_values = range(255, -1, -5)
        df_shift_jis = colorize_column(df_shift_jis, col_idx, color_values)

    # 表示
    st.dataframe(df_shift_jis)

