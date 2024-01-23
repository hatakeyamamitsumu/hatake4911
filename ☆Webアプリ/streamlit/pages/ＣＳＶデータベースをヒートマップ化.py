import streamlit as st
import pandas as pd
import seaborn as sns
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

    # ファイルアップロードウィジェットを追加
    st.subheader("CSVファイルアップロード")
    uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

    # ファイルがアップロードされた場合の処理
    if uploaded_file is not None:
        # ファイルを読み込む
        encoding = 'utf-8'  # デフォルトはUTF-8
        df = read_file(uploaded_file, encoding)

        # データが読み込まれた場合の処理
        if df is not None:
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

if __name__ == "__main__":
    main()
