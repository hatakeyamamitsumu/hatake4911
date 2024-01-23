import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns

def read_file(file, encoding):
    try:
        content = file.read()
        decoded_content = content.decode(encoding)
        df = pd.read_csv(pd.compat.StringIO(decoded_content))
        return df
    except Exception as e:
        st.error(f"ファイルを読み込む際にエラーが発生しました: {str(e)}")
        return None

def generate_colored_table(df):
    st.subheader("色付きテーブル")

    # 数値の列を取得
    numerical_columns = df.select_dtypes(include=[np.number]).columns

    # 色のスケールを設定
    cmap = sns.color_palette("coolwarm", as_cmap=True)

    # テーブルのスタイルを設定
    styles = []
    for col in numerical_columns:
        style = df[col].apply(lambda x: f"background-color: {sns.color_palette('coolwarm', as_cmap=True)(x)}", axis=0)
        styles.append(style)

    # スタイルを結合して表示
    styled_df = df.style.apply(lambda x: np.concatenate(styles, axis=1), axis=None)
    st.dataframe(styled_df, unsafe_allow_html=True)

def main():
    st.title("色付きテーブルアプリ")

    # UTF-8 ファイルアップロードウィジェット
    st.subheader("UTF-8 ファイルアップロード")
    utf8_file = st.file_uploader("UTF-8 エンコーディングの CSV ファイルをアップロードしてください", type=["csv"])

    if utf8_file is not None:
        st.write("UTF-8 エンコーディングのデータ:")
        df_utf8 = read_file(utf8_file, 'utf-8')

        if df_utf8 is not None:
            st.subheader("データの概要")
            st.write(df_utf8)
            generate_colored_table(df_utf8)

    # Shift-JIS ファイルアップロードウィジェット
    st.subheader("Shift-JIS ファイルアップロード")
    sjis_file = st.file_uploader("Shift-JIS エンコーディングの CSV ファイルをアップロードしてください", type=["csv"])

    if sjis_file is not None:
        st.write("Shift-JIS エンコーディングのデータ:")
        df_sjis = read_file(sjis_file, 'shift-jis')

        if df_sjis is not None:
            st.subheader("データの概要")
            st.write(df_sjis)
            generate_colored_table(df_sjis)

if __name__ == "__main__":
    main()

