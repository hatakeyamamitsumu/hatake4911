import streamlit as st
import pandas as pd
import numpy as np

def read_csv_utf8(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

def read_csv_shift_jis(uploaded_file):
    df = pd.read_csv(uploaded_file, encoding='shift-jis')
    return df

# ページのタイトル
st.title("CSVデータの数値列を降順に着色表示")

# UTF-8用アップローダー
uploaded_file_utf8 = st.file_uploader("UTF-8エンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_utf8 is not None:
    st.subheader("UTF-8データフレーム")
    df_utf8 = read_csv_utf8(uploaded_file_utf8)

    # 数値列だけを取得
    numeric_columns_utf8 = df_utf8.select_dtypes(include='number').columns.tolist()

    if not numeric_columns_utf8:
        st.warning("数値列が見つかりませんでした。")
    else:
        # 数値列を降順にソートして、着色
        for col in numeric_columns_utf8:
            df_utf8[col] = df_utf8[col].sort_values(ascending=False).rank(method='first', ascending=False) * 5

        # 着色
        st.dataframe(df_utf8.style.apply(lambda x: [f'background-color: rgb({255 - int(min(255, x[i] * 5))}, 0, 0)' for i in range(len(x))]))

# Shift-JIS用アップローダー
uploaded_file_shift_jis = st.file_uploader("Shift-JISエンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_shift_jis is not None:
    st.subheader("Shift-JISデータフレーム")
    df_shift_jis = read_csv_shift_jis(uploaded_file_shift_jis)

    # 数値列だけを取得
    numeric_columns_shift_jis = df_shift_jis.select_dtypes(include='number').columns.tolist()

    if not numeric_columns_shift_jis:
        st.warning("数値列が見つかりませんでした。")
    else:
        # 数値列を降順にソートして、着色
        for col in numeric_columns_shift_jis:
            df_shift_jis[col] = df_shift_jis[col].sort_values(ascending=False).rank(method='first', ascending=False) * 5

        # 着色
        st.dataframe(df_shift_jis.style.apply(lambda x: [f'background-color: rgb({255 - int(min(255, x[i] * 5))}, 0, 0)' for i in range(len(x))]))
