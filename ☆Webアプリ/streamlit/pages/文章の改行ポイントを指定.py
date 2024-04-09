import streamlit as st
import re

def main():
    st.title("文章を指定した文字の前後で改行")
    st.write("文章を、選択した文字の前後で改行し、見やすくします。文章選別の前準備としてご利用ください")

    # アップロードされたテキストファイルを取得
    uploaded_file = st.file_uploader("テキストファイルをアップロードしてください")

    # ユーザーが入力した区切り文字（スペースで区切って複数入力）
    st.write("1：指定した文字の手前で改行します。")
    st.write("例：「　｛ [　結論　その他　")
    custom_delimiters = st.text_input("改行したい文字をスペースで区切って入力してください", key="delimiters")

    # ユーザーが入力したピリオド（スペースで区切って複数入力）
    st.write("2：指定した文字の後ろで改行します。")
    st.write("例：」　｝　]　.　． 。")
    custom_periods = st.text_input("改行したい文字をスペースで区切って入力してください", key="periods")

    # テキストファイルの内容を読み込み
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")

        # 選択したピリオドを正規表現パターンに組み込む
        period_pattern = "|".join(map(re.escape, custom_periods.split()))

        # 選択した区切り文字を正規表現パターンに組み込む
        delimiter_pattern = "|".join(map(re.escape, custom_delimiters.split()))

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
                if split_text[i-1] in custom_periods.split():
                    formatted_text.append("\n" + split_text[i])
                # 区切り文字の直前なら改行を追加
                elif split_text[i] in custom_delimiters.split():
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
