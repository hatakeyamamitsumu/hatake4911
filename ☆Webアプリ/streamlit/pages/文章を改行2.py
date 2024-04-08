import streamlit as st
import re
import base64

def main():
    st.title("文章を指定の文字の前後で改行")
    st.write("文章を、選択した文字の前後で改行し、見やすくします。文章選別の前準備としてご利用ください")

    # アップロードされたテキストファイルを取得
    uploaded_file = st.file_uploader("テキストファイルをアップロードしてください")
    
    # ユーザーが選択した区切り文字（複数選択可）
    st.write("**1：指定した文字の前で改行**")
    selected_delimiters = st.multiselect("改行用の文字を選択してください(複数選択可)", ["「","(","（","＜","<","[","｛","{"])
    
    # ユーザーが選択したピリオド（複数選択可）
    st.write("**2：指定した文字の後で改行**")
    selected_periods = st.multiselect("改行用の文字を選択してください(複数選択可)", ["。", "．", ".", "、", ",", "」", ")", "）","＞",">","]","｝","}"])

    # ユーザーが入力した任意の単語
    custom_word = st.text_input("任意の単語を入力してください")

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
                # 任意の単語の直前なら改行を追加
                elif split_text[i-1] == custom_word:
                    formatted_text.append("\n" + split_text[i])
                else:
                    formatted_text.append(split_text[i])

        # ダウンロードボタン
        if st.button("ダウンロードしますか？"):
            # ダウンロードファイル名
            filename = "分割結果.txt"

            # ダウンロードファイルの内容
            content = "".join(formatted_text)

            # Base64エンコード
            b64 = base64.b64encode(content.encode()).decode()
            href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">ダウンロード</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
