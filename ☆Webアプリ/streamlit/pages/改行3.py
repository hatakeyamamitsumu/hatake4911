import streamlit as st
import re

def main():
    st.title("文章をピリオドで改行")
    st.write("文章を指定したピリオドの直前で改行します")

    # アップロードされたテキストファイルを取得
    uploaded_file = st.file_uploader("テキストファイルを選択してください")

    # ユーザーが選択したピリオド（複数選択可）
    selected_periods = st.multiselect("ピリオドを選択してください(複数選択可)", ["。", "．", ".", "、", ",", "「"])

    # テキストファイルの内容を読み込み
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")

        # 選択したピリオドを正規表現パターンに組み込む
        pattern = "|".join(map(re.escape, selected_periods))

        # テキストファイルを選択したピリオドで分割
        split_text = re.split(f"({pattern})", text)
        
        # 分割結果の整形
        formatted_text = []
    for i in range(len(split_text)):
        # 最後の要素の場合は、ピリオドの直前で改行を追加
        if i == len(split_text) - 1 and split_text[i] in selected_periods:
            formatted_text.append("\n" + split_text[i])
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
