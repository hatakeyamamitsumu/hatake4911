import streamlit as st
import re

def main():
    # アップロードされたテキストファイルを取得
    uploaded_file = st.file_uploader("テキストファイルを選択してください")

    # テキストファイルの内容を読み込み
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")

        # テキストファイルを「。」「.」「．」で分割
        split_text = re.split(r"(?<=[。．\.])", text)

        # ダウンロードボタン
        if st.button("ダウンロード"):
            # ダウンロードファイル名
            filename = "分割結果.txt"

            # ダウンロードファイルの内容
            content = "\r\n".join(split_text)

            # ダウンロード処理
            st.download_button(
                label="ダウンロード",
                data=content,
                file_name=filename,
                mime="text/plain",
            )

if __name__ == "__main__":
    main()
