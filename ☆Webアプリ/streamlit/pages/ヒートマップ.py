import streamlit as st
import pandas as pd

def read_csv_shift_jis(uploaded_file):
    df = pd.read_csv(uploaded_file, encoding='shift-jis')
    return df

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
        max_values_shift_jis = df_shift_jis[numeric_columns_shift_jis].max()

        # 各列の最大値に対応するセルにスタイルを適用する関数
        def highlight_max_shift_jis(s):
            if s.name in max_values_shift_jis:
                is_max = s == max_values_shift_jis[s.name]
                return ['background-color: red' if v else '' for v in is_max]
            else:
                return [''] * len(s)

        # 表示
        st.dataframe(df_shift_jis.style.apply(highlight_max_shift_jis, axis=0))
