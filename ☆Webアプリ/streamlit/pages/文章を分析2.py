import streamlit as st
import pandas as pd
from docx import Document
import os

def read_word_file(file):
    doc = Document(file)
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    return text

def read_filter_words_from_csv(file_path):
    filter_words_df = pd.read_csv(file_path)
    filter_words = filter_words_df['単語'].tolist()
    return filter_words

def filter_and_display(text, filter_words):
    lines_with_filter_words = [line for line in text.split('\n') if any(word.lower() in line.lower() for word in filter_words)]

    if lines_with_filter_words:
        result_df = pd.DataFrame({"行": lines_with_filter_words})
        st.write("ＣＳＶファイル内の単語を含む行のリスト")
        st.dataframe(result_df)
    else:
        st.write(f"テキストにＣＳＶファイル内の単語を含む行は見つかりませんでした。")

def main():
    st.title("文章フィルター")

    uploaded_file = st.file_uploader("テキストファイルまたはワードファイルをアップロードしてください", type=["txt", "docx"])

    filter_folder_path = "/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/文章分析用CSV"
    filter_file_name = st.selectbox("CSV ファイルを選択してください", sorted(os.listdir(filter_folder_path)))

    filter_file_path = os.path.join(filter_folder_path, filter_file_name)

    if uploaded_file is not None:
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = read_word_file(uploaded_file)
        else:
            text = uploaded_file.read().decode("utf-8")

        filter_words = read_filter_words_from_csv(filter_file_path)

        if filter_words:
            filter_and_display(text, filter_words)

if __name__ == "__main__":
    main()

