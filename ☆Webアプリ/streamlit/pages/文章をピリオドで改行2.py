import streamlit as st
import re

def main():
    st.title("文章をピリオドまたは区切り文字で改行")
    st.write("文章を指定したピリオドまたは区切り文字の直後で改行します")

    # アップロードされたテキストファイルを取得
    uploaded_file = st.file_uploader("テキストファイルを選択してください")

    # ユーザーが選択したピリオド（複数選択可）
    selected_periods = st.multiselect("ピリオドを選択してください(複数選択可)", ["。", "．", ".", "、", ",", "」"])

    # ユーザーが選択した区切り文字（複数選択可）
    selected_delimiters = st.multiselect("区切り文字を選択してください(複数選択可)", ["の", "その", "これ", "あれ"])

    # テキストファイルの内容を読み込み
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")

        # 選択したピリオドを正規表現パターンに組み込む
        period_pattern = "|".join(map(re.escape, selected_periods))

        # 選択した区切り文字を正規表現パターンに組み込む
        delimiter_pattern = "|".join(map(re.escape, selected_delimiters))

        # テキストファイルを選択したピリオドと区切り文字で分割
        split_text = re.split(f"({period_pattern}|{delimiter_pattern})", text)

        # 分割結果の整形
        formatted_text = []
        for i in range(len(split_text)):
            # 最初の要素は追加だけ
            if i == 0:
                formatted_text.append(split_text[i])
            else:
                # 区切り文字の直前で改行を追加
                if i > 0 and split_text[i] in selected_delimiters:
                    formatted_text[-1] += "\n"
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

