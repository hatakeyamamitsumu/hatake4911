import streamlit as st
import pandas as pd

def read_csv_utf8(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

def read_csv_shift_jis(uploaded_file):
    df = pd.read_csv(uploaded_file, encoding='shift-jis')
    return df

# ページのタイトル
st.title("CSVデータの列を降順にソートし、上位i番目のセルを着色")

# RGBの色の定義
def get_color(i):
    return f'rgb({255 - min(i, 25) * 10}, 0, 0)'

# UTF-8用アップローダー
uploaded_file_utf8 = st.file_uploader("UTF-8エンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_utf8 is not None:
    st.subheader("UTF-8データフレーム")
    df_utf8 = read_csv_utf8(uploaded_file_utf8)

    # 列ごとに処理
    for i, column in enumerate(df_utf8.columns):
        st.subheader(f"列: {column}")

        # 列を降順にソート
        sorted_df = df_utf8.sort_values(by=column, ascending=False)

        # 上からi番目のセルに色を付ける
        sorted_column_color = sorted_df.style.apply(lambda x: f'background-color: {get_color(i)}' if x.name == column else '', axis=0)
        
        # 表示
        st.dataframe(sorted_column_color)

# Shift-JIS用アップローダー
uploaded_file_shift_jis = st.file_uploader("Shift-JISエンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_shift_jis is not None:
    st.subheader("Shift-JISデータフレーム")
    df_shift_jis = read_csv_shift_jis(uploaded_file_shift_jis)

    # 列ごとに処理
    for i, column in enumerate(df_shift_jis.columns):
        st.subheader(f"列: {column}")

        # 列を降順にソート
        sorted_df = df_shift_jis.sort_values(by=column, ascending=False)

        # 上からi番目のセルに色を付ける
        sorted_column_color = sorted_df.style.apply(lambda x: f'background-color: {get_color(i)}' if x.name == column else '', axis=0)
        
        # 表示
        st.dataframe(sorted_column_color)



