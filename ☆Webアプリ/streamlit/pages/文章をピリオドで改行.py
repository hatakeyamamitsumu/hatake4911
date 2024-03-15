import streamlit as st
import re

def main():
    st.title("文章をピリオドで改行")
    st.write("文章を「。」「．」「.」を境に改行します。")
    
    # アップロードされたテキストファイルを取得
    uploaded_file = st.file_uploader("テキストファイルを選択してください")

    # テキストファイルの内容を読み込み
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")

        # テキストファイルを「。」「.」「．」で分割
        split_text = re.split(r"([。．\.])", text)
        
        # 分割結果の整形
        formatted_text = []
        for i in range(len(split_text)):
            # 最後の要素は追加だけ
            if i == len(split_text) - 1:
                formatted_text.append(split_text[i])
            else:
                # ピリオドの直後なら改行を追加
                if split_text[i] in ["。", "．", "."]:
                    formatted_text.append(split_text[i] + "\n")
                else:
                    formatted_text.append(split_text[i])

        # ダウンロードボタン
        if st.button("ダウンロードしますか？"):
            # ダウンロードファイル名
            filename = "分割結果.txt"

            # ダウンロードファイルの内容
            content = "".join(formatted_text)

            # ダウンロード処理
            st.download_button(
                label="ダウンロードボタン",
                data=content,
                file_name=filename,
                mime="text/plain",
            )

if __name__ == "__main__":
    main()
