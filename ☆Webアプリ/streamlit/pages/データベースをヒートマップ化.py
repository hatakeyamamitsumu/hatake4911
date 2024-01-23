import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ページのタイトルを設定
st.title("CSVデータのヒートマップ表示")

# ファイルアップロードのウィジェットを追加
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

# CSVファイルがアップロードされた場合の処理
if uploaded_file is not None:
    # アップロードされたファイルをDataFrameに読み込む
    df = pd.read_csv(uploaded_file)

    # データの概要を表示
    st.subheader("データの概要")
    st.write(df)

    # ヒートマップを作成して表示
    st.subheader("ヒートマップ")
    sns.set()
    plt.figure(figsize=(10, 8))
    heatmap = sns.heatmap(df.corr(), annot=True, cmap="coolwarm", linewidths=.5)
    st.pyplot()

    # データの統計情報を表示
    st.subheader("データの統計情報")
    st.write(df.describe())
else:
    st.warning("CSVファイルをアップロードしてください。")
