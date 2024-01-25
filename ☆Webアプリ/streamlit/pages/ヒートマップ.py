import streamlit as st
import pandas as pd
import numpy as np

def read_csv_utf8(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

def read_csv_shift_jis(uploaded_file):
    df = pd.read_csv(uploaded_file, encoding='shift-jis')
    return df

def generate_gradient(value, max_value):
    normalized_value = min(value, max_value) / max_value
    red = max(0, int(255 - normalized_value * 255))
    green = 0
    blue = 0
    return f'background-color: rgb({red}, {green}, {blue})'

# Gradient highlighting function
def highlight_gradient(s):
    if s.name in max_values:
        max_value = max_values[s.name]
        return [generate_gradient(v, max_value) for v in s]
    else:
        return [''] * len(s)

# ページのタイトル
st.title("CSVデータの最大値をグラデーション表示")

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
        # 各列の最大値を取得
        max_values = df_utf8[numeric_columns_utf8].max()

        # 表示
        st.dataframe(df_utf8.style.apply(highlight_gradient, axis=0))

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
        # 各列の最大値を取得
        max_values = df_shift_jis[numeric_columns_shift_jis].max()

        # 表示
        st.dataframe(df_shift_jis.style.apply(highlight_gradient, axis=0))
