import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ページのタイトルを設定
st.title("列ごとの最大値と最小値を示すヒートマップ")

# ファイルアップロードのウィジェットを追加
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

# CSVファイルがアップロードされた場合の処理
if uploaded_file is not None:
    # アップロードされたファイルをDataFrameに読み込む
    df = pd.read_csv(uploaded_file)

    # データの概要を表示
    st.subheader("データの概要")
    st.write(df)

    # 各列の最大値と最小値を取得
    min_values = df.min()
    max_values = df.max()

    # ヒートマップを作成して表示
    st.subheader("ヒートマップ")
    sns.set()
    plt.figure(figsize=(10, 8))
    
    # ヒートマップの作成
    heatmap_data = (df - min_values) / (max_values - min_values)
    heatmap = sns.heatmap(heatmap_data, cmap="coolwarm", linewidths=.5, annot=True)
    st.pyplot()

    # データの統計情報を表示
    st.subheader("データの統計情報")
    st.write(df.describe())
else:
    st.warning("CSVファイルをアップロードしてください。")
