import streamlit as st
import pandas as pd
import io

def read_csv_utf8(uploaded_file):
    content = uploaded_file.read()
    decoded_content = content.decode("utf-8")
    df = pd.read_csv(io.StringIO(decoded_content))
    return df

def read_csv_shift_jis(uploaded_file):
    content = uploaded_file.read()
    decoded_content = content.decode("shift-jis")
    df = pd.read_csv(io.StringIO(decoded_content))
    return df

st.title("CSVファイルアップローダー")

# UTF-8用のアップローダー
uploaded_file_utf8 = st.file_uploader("UTF-8エンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_utf8 is not None:
    st.subheader("UTF-8データフレーム")
    df_utf8 = read_csv_utf8(uploaded_file_utf8)
    st.write(df_utf8)

# Shift-JIS用のアップローダー
uploaded_file_shift_jis = st.file_uploader("Shift-JISエンコーディングのCSVファイルをアップロードしてください", type=["csv"])
if uploaded_file_shift_jis is not None:
    st.subheader("Shift-JISデータフレーム")
    df_shift_jis = read_csv_shift_jis(uploaded_file_shift_jis)
    st.write(df_shift_jis)
