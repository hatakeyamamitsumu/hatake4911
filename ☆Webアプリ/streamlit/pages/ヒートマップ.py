import streamlit as st
import pandas as pd

def read_csv(uploaded_file, encoding=None):
    df = pd.read_csv(uploaded_file, encoding=encoding)
    return df

def colorize_column(df, col_idx, color_values):
    col_name = df.columns[col_idx]
    if pd.api.types.is_numeric_dtype(df[col_name]):
        df[col_name] = df[col_name].sort_values(ascending=False).rank(method='first', ascending=False) * 5
        for i, color in enumerate(color_values):
            df.style.applymap(lambda x: f'background-color: rgb({color}, 0, 0)', subset=pd.IndexSlice[0:i, col_name])

# ページのタイトル
st.title("CSVデータの数値列を着色表示")

# アップローダー
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])
if uploaded_file is not None:
    df = read_csv(uploaded_file)

    # 列ごとに処理
    for col_idx in range(df.shape[1]):
        color_values = range(255, -1, -5)
        colorize_column(df, col_idx, color_values)

    # 表示
    st.dataframe(df)
