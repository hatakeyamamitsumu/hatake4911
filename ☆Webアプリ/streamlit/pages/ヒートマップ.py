import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def read_csv(uploaded_file, encoding):
    df = pd.read_csv(uploaded_file, encoding=encoding)
    return df

def highlight_cells(df):
    styled_df = df.copy()
    num_cols = df.shape[1]

    for i in range(num_cols):
        selected_col = df.iloc[:, i].sort_values(ascending=False)
        for j in range(1, 26):
            if j == 25:
                break

            color = f'rgb({255 - j * 10}, 0, 0)'
            idx_to_highlight = selected_col.index[j - 1]
            styled_df.at[idx_to_highlight, i] = f'<mark style="background-color: {color}">{styled_df.at[idx_to_highlight, i]}</mark>'

    return styled_df

# ページのタイトル
st.title("CSVデータベースのセルを着色で強調表示")

# UTF-8用アップローダー
uploaded_file_utf8 = st.file_uploader("UTF-8エンコーディングのCSVファイルをアップロードしてください", type=["csv"])

# Shift-JIS用アップローダー
uploaded_file_shift_jis = st.file_uploader("Shift-JISエンコーディングのCSVファイルをアップロードしてください", type=["csv"])

# UTF-8データベースの処理
if uploaded_file_utf8 is not None:
    st.subheader("UTF-8データベース")
    df_utf8 = read_csv(uploaded_file_utf8, 'utf-8')

    # Matplotlib colormap
    matplot_color = df_utf8.style.background_gradient(cmap='viridis')
    st.write(matplot_color)

    # Seaborn colorpalette
    cm = sns.light_palette("green", as_cmap=True)
    sns_color = df_utf8.style.background_gradient(cmap=cm)
    st.write(sns_color)

    # Seaborn colorpalette + nanを黒にする
    sns_color_nan = df_utf8.style.background_gradient(cmap=cm).highlight_null('black')
    st.write(sns_color_nan)

# Shift-JISデータベースの処理
if uploaded_file_shift_jis is not None:
    st.subheader("Shift-JISデータベース")
    df_shift_jis = read_csv(uploaded_file_shift_jis, 'shift-jis')

    # Matplotlib colormap
    matplot_color = df_shift_jis.style.background_gradient(cmap='viridis')
    st.write(matplot_color)

    # Seaborn colorpalette
    cm = sns.light_palette("green", as_cmap=True)
    sns_color = df_shift_jis.style.background_gradient(cmap=cm)
    st.write(sns_color)

    # Seaborn colorpalette + nanを黒にする
    sns_color_nan = df_shift_jis.style.background_gradient(cmap=cm).highlight_null('black')
    st.write(sns_color_nan)

