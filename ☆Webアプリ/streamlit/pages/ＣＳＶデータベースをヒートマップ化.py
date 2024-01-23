import streamlit as st
import pandas as pd
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
    st.title("CSVファイル読み込みアプリ")

    # ファイルアップロードウィジェットを追加（UTF-8用）
    st.subheader("UTF-8ファイルアップロード")
    utf8_file = st.file_uploader("UTF-8エンコーディングのCSVファイルをアップロードしてください", type=["csv"])

    # UTF-8ファイルがアップロードされた場合の処理
    if utf8_file is not None:
        st.write("UTF-8エンコーディングのデータ:")
        df_utf8 = read_file(utf8_file, 'utf-8')
        if df_utf8 is not None:
            st.write(df_utf8)

    # ファイルアップロードウィジェットを追加（Shift-JIS用）
    st.subheader("Shift-JISファイルアップロード")
    sjis_file = st.file_uploader("Shift-JISエンコーディングのCSVファイルをアップロードしてください", type=["csv"])

    # Shift-JISファイルがアップロードされた場合の処理
    if sjis_file is not None:
        st.write("Shift-JISエンコーディングのデータ:")
        df_sjis = read_file(sjis_file, 'shift-jis')
        if df_sjis is not None:
            st.write(df_sjis)

if __name__ == "__main__":
    main()
