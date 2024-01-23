import streamlit as st
import pandas as pd
import numpy as np

# CSVファイルのアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

if uploaded_file is not None:
    # CSVデータを読み込む
    df = pd.read_csv(uploaded_file)

    # 各列のデータ型を確認し、数値列だけを取得
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

    # 各列の最大値を取得
    max_values = df[numeric_columns].max()

    # 各列の最大値に対応するセルにスタイルを適用する関数
    def highlight_max(s):
        is_max = s == max_values[s.name]
        return ['background-color: red' if v else '' for v in is_max]

    # 表示
    st.dataframe(df.style.apply(highlight_max, axis=0))
