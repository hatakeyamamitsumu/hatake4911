import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

def read_file(file, encoding):
    # ファイルをDataFrameに読み込み
    try:
        # ファイルの中身をバイト列として取得
        content = file.read()

        # バイト列を文字列にデコード
        decoded_content = content.decode(encoding)

        # 文字列からDataFrameを作成
        df = pd.read_csv(io.StringIO(decoded_content))
        
        return df
    except Exception as e:
        st.error(f"ファイルを読み込む際にエラーが発生しました: {str(e)}")
        return None

def main():
    st.title("CSVファイル読み込み＆ヒートマップアプリ")

    # ファイルアップロードウィジェットを追加（UTF-8用）
    st.subheader("UTF-8ファイルアップロード")
    utf8_file = st.file_uploader("UTF-8エンコーディングのCSVファイルをアップロードしてください", type=["csv"])

    # UTF-8ファイルがアップロードされた場合の処理
    if utf8_file is not None:
        st.write("UTF-8エンコーディングのデータ:")
        df_utf8 = read_file(utf8_file, 'utf-8')
        if df_utf8 is not None:
            # データの概要を表示
            st.subheader("データの概要")
            st.write(df_utf8)

            # 各列の最大値と最小値を取得
            min_values_utf8 = df_utf8.min()
            max_values_utf8 = df_utf8.max()

            # ヒートマップを作成して表示
            st.subheader("ヒートマップ (UTF-8)")
            sns.set()
            plt.figure(figsize=(10, 8))
            
            # ヒートマップの作成
            heatmap_data_utf8 = (df_utf8 - min_values_utf8) / (max_values_utf8 - min_values_utf8)
            heatmap_utf8 = sns.heatmap(heatmap_data_utf8, cmap="coolwarm", linewidths=.5, annot=True)
            st.pyplot()

            # データの統計情報を表示
            st.subheader("データの統計情報 (UTF-8)")
            st.write(df_utf8.describe())

    # ファイルアップロードウィジェットを追加（Shift-JIS用）
    st.subheader("Shift-JISファイルアップロード")
    sjis_file = st.file_uploader("Shift-JISエンコーディングのCSVファイルをアップロードしてください", type=["csv"])

    # Shift-JISファイルがアップロードされた場合の処理
    if sjis_file is not None:
        st.write("Shift-JISエンコーディングのデータ:")
        df_sjis = read_file(sjis_file, 'shift-jis')
        if df_sjis is not None:
            # データの概要を表示
            st.subheader("データの概要")
            st.write(df_sjis)

            # 各列の最大値と最小値を取得
            min_values_sjis = df_sjis.min()
            max_values_sjis = df_sjis.max()

            # ヒートマップを作成して表示
            st.subheader("ヒートマップ (Shift-JIS)")
            plt.figure(figsize=(10, 8))
            
            # ヒートマップの作成
            heatmap_data_sjis = (df_sjis - min_values_sjis) / (max_values_sjis - min_values_sjis)
            heatmap_sjis = sns.heatmap(heatmap_data_sjis, cmap="coolwarm", linewidths=.5, annot=True)
            st.pyplot()

            # データの統計情報を表示
            st.subheader("データの統計情報 (Shift-JIS)")
            st.write(df_sjis.describe())

if __name__ == "__main__":
    main()
