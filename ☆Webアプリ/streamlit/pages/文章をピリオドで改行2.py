import streamlit as st
import re

def main():
    st.title("文章をピリオドで改行、区切り文字の前で改行")
    st.write("文章を指定したピリオドの直後で改行し、区切り文字の直前で改行します")

    # アップロードされたテキストファイルを取得
    uploaded_file = st.file_uploader("テキストファイルを選択してください")

    # ユーザーが選択したピリオド（複数選択可）
    selected_periods = st.multiselect("後改行用の文字を選択してください(複数選択可)", ["。", "．", ".", "、", ",", "」"])

    # ユーザーが選択した区切り文字（複数選択可）
    selected_delimiters = st.multiselect("前改行用の文字を選択してください(複数選択可)", ["「"])

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
                # ピリオドの直後なら改行を追加
                if split_text[i-1] in selected_periods:
                    formatted_text.append("\n" + split_text[i])
                # 区切り文字の直前なら改行を追加
                elif split_text[i] in selected_delimiters:
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
