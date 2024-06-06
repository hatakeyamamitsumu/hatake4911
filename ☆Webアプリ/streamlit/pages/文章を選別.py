import streamlit as st
import pandas as pd
from docx import Document
import os
import re

def count_words(text):
    words = text.split()
    word_counts = dict(pd.Series(words).value_counts())
    return word_counts

def read_word_file(file):
    doc = Document(file)
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    return text

def filter_and_download(text, filter_words, filter_condition):
    if filter_condition == 'and':
        lines_with_words = [line for line in text.split('\n') if all(word.lower() in line.lower() for word in filter_words)]
    elif filter_condition == 'or':
        lines_with_words = [line for line in text.split('\n') if any(word.lower() in line.lower() for word in filter_words)]
    elif filter_condition == 'not':
        lines_with_words = [line for line in text.split('\n') if all(word.lower() not in line.lower() for word in filter_words)]
    else:
        st.error("無効な条件が選択されました。'and', 'or', または 'not' を選択してください。")
        return

    if lines_with_words:
        result_df = pd.DataFrame({"行": lines_with_words})
        st.write(f"### '{', '.join(filter_words)}' を含む行のリスト ({filter_condition} 条件)")
        st.dataframe(result_df)

        result_text = "\n".join(lines_with_words)
        file_name = "filtered_data.txt"
        st.download_button(label="テキストファイルとしてダウンロード", data=result_text, file_name=file_name, key="download_button")
    else:
        st.write(f"テキストに '{', '.join(filter_words)}' を含む行は見つかりませんでした。")

def read_filter_words_from_csv(file_path):
    filter_words_df = pd.read_csv(file_path)
    filter_words = filter_words_df['単語'].tolist()
    return filter_words

def filter_and_display(text, filter_words):
    lines_with_filter_words = [line for line in text.split('\n') if any(word.lower() in line.lower() for word in filter_words)]

    if lines_with_filter_words:
        result_df = pd.DataFrame({"行": lines_with_filter_words})
        st.write("単語帳の中の単語を含む行のリスト")
        st.dataframe(result_df)

        filtered_text = "\n".join(lines_with_filter_words)
        st.download_button(label="テキストファイルとしてダウンロード", data=filtered_text, file_name="filtered_data.txt", key="text_file")
    else:
        st.write(f"単語帳の中の単語を含む行は見つかりませんでした.")

def split_text_around_delimiters(text, custom_delimiters, custom_periods):
    period_pattern = "|".join(map(re.escape, custom_periods.split()))
    delimiter_pattern = "|".join(map(re.escape, custom_delimiters.split()))

    split_text = re.split(f"({period_pattern}|{delimiter_pattern})", text)
    formatted_text = []
    for i in range(len(split_text)):
        if i == 0:
            formatted_text.append(split_text[i])
        else:
            if split_text[i-1] in custom_periods.split():
                formatted_text.append("\n" + split_text[i])
            elif split_text[i] in custom_delimiters.split():
                formatted_text.append("\n" + split_text[i])
            else:
                formatted_text.append(split_text[i])
    return "".join(formatted_text)

def main():
    st.title("テキスト処理アプリケーション")

    app_selection = st.sidebar.radio("アプリを選択してください", 
                                     ("入力した単語でフィルタリング", "CSVファイルから単語リストでフィルタリング", "指定した文字の前後で改行"))

    uploaded_file = st.file_uploader("テキストファイルまたはワードファイルをアップロードしてください", type=["txt", "docx"])

    if uploaded_file is not None:
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = read_word_file(uploaded_file)
        else:
            text = uploaded_file.read().decode("utf-8")

        if app_selection == "入力した単語でフィルタリング":
            st.write("複数の単語を入力し、その語が含まれる行を抽出するアプリです。")
            word_counts = count_words(text)
            result_df = pd.DataFrame(list(word_counts.items()), columns=['単語', '出現回数'])
            st.write("### 原本")
            st.dataframe(result_df)

            filter_words = st.text_area("抽出したい語をスペースで区切って入力してください。例：山　川　歩　泳　しかし　まあまあ")
            filter_condition = st.radio("条件を選択してください:", ['and', 'or', 'not'])

            if filter_words:
                filter_words = filter_words.split()
                filter_and_download(text, filter_words, filter_condition)

        elif app_selection == "CSVファイルから単語リストでフィルタリング":
            st.write("私があらかじめ単語帳に集めた５０～１００個の単語が含まれる行を抽出するアプリです。")
            filter_folder_path = "/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/文章分析用CSV"
            filter_file_name = st.selectbox("単語帳を選択してください", sorted(os.listdir(filter_folder_path)))

            filter_file_path = os.path.join(filter_folder_path, filter_file_name)
            filter_words = read_filter_words_from_csv(filter_file_path)

            if filter_words:
                filter_and_display(text, filter_words)

        elif app_selection == "指定した文字の前後で改行":
            st.write("文章を、入力した文字の前後で改行し、見やすくします。文章選別の前準備としてご利用ください")

            custom_delimiters = st.text_input("改行したい文字をスペースで区切って入力してください", key="delimiters")
            custom_periods = st.text_input("改行したい文字をスペースで区切って入力してください", key="periods")

            if custom_delimiters or custom_periods:
                formatted_text = split_text_around_delimiters(text, custom_delimiters, custom_periods)

                if st.button("ダウンロードしますか？"):
                    filename = "分割結果.txt"
                    st.download_button(label="ダウンロードボタン", data=formatted_text, file_name=filename, mime="text/plain")

if __name__ == "__main__":
    main()
