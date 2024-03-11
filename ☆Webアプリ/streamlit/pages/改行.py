import streamlit as st
import re

def main():
    # アップロードされたテキストファイルを取得
    uploaded_file = st.file_uploader("テキストファイルを選択してください")

    # テキストファイルの内容を読み込み
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")

        # テキストファイルを「。」「.」「．」で分割
        split_text = re.split(r"[。.．]", text)

        # 分割された結果を改行して表示
        for sentence in split_text:
            st.write(sentence + "\r\n")

if __name__ == "__main__":
    main()

