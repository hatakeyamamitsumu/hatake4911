import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

def read_file(file, encoding):
    try:
        content = file.read()
        decoded_content = content.decode(encoding)
        df = pd.read_csv(io.StringIO(decoded_content))
        return df
    except Exception as e:
        st.error(f"ファイルを読み込む際にエラーが発生しました: {str(e)}")
        return None

def generate_heatmap(df):
    st.subheader("ヒートマップ")

    # 各数値列の最小値と最大値を取得
    min_values = df.select_dtypes(include=['number']).min()
    max_values = df.select_dtypes(include=['number']).max()

    sns.set()
    plt.figure(figsize=(10, 8))

    # ヒートマップの作成
    heatmap_data = df.select_dtypes(include=['number']).apply(lambda x: (x - min_values) / (max_values - min_values))
    heatmap = sns.heatmap(heatmap_data, cmap="coolwarm", linewidths=.5, annot=True)
    st.pyplot()

    st.subheader("データの統計情報")
    st.write(df.describe())

def main():
    st.title("CSVファイル読み込み＆ヒートマップアプリ")

    # UTF-8 ファイルアップロードウィジェット
    st.subheader("UTF-8 ファイルアップロード")
    utf8_file = st.file_uploader("UTF-8 エンコーディングの CSV ファイルをアップロードしてください", type=["csv"])

    if utf8_file is not None:
        st.write("UTF-8 エンコーディングのデータ:")
        df_utf8 = read_file(utf8_file, 'utf-8')

        if df_utf8 is not None:
            st.subheader("データの概要")
            st.write(df_utf8)
            generate_heatmap(df_utf8)

    # Shift-JIS ファイルアップロードウィジェット
    st.subheader("Shift-JIS ファイルアップロード")
    sjis_file = st.file_uploader("Shift-JIS エンコーディングの CSV ファイルをアップロードしてください", type=["csv"])

    if sjis_file is not None:
        st.write("Shift-JIS エンコーディングのデータ:")
        df_sjis = read_file(sjis_file, 'shift-jis')

        if df_sjis is not None:
            st.subheader("データの概要")
            st.write(df_sjis)
            generate_heatmap(df_sjis)

if __name__ == "__main__":
    main()

