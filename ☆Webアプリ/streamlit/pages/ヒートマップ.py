import streamlit as st
import pandas as pd
import numpy as np

def read_csv_utf8(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

def read_csv_shift_jis(uploaded_file):
    df = pd.read_csv(uploaded_file, encoding='shift-jis')
    return df

def highlight_gradient(s, cmap='Reds'):
    # Normalize the values in the column
    normalized_values = (s - s.min()) / (s.max() - s.min())
    
    # Map the normalized values to a color gradient
    color_gradient = st.color_gradient(np.nan_to_num(normalized_values), cmap=cmap)

    # Apply the color gradient to each cell
    return [f'background-color: {color}' for color in color_gradient]

# ページのタイトル
st.title("CSVデータの列にグラデーションを適用")

# UTF-8用アップローダー
uploaded_file_utf8 = st.file_uploader("UTF-8エンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_utf8 is not None:
    st.subheader("UTF-8データフレーム")
    df_utf8 = read_csv_utf8(uploaded_file_utf8)

    # 各列にグラデーションを適用する
    st.dataframe(df_utf8.style.apply(highlight_gradient, cmap='Reds', axis=0))

# Shift-JIS用アップローダー
uploaded_file_shift_jis = st.file_uploader("Shift-JISエンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_shift_jis is not None:
    st.subheader("Shift-JISデータフレーム")
    df_shift_jis = read_csv_shift_jis(uploaded_file_shift_jis)

    # 各列にグラデーションを適用する
    st.dataframe(df_shift_jis.style.apply(highlight_gradient, cmap='Blues', axis=0))

