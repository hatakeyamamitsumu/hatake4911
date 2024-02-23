import streamlit as st
import pandas as pd
from io import StringIO
from docx import Document
import re

def count_words(text):
    words = text.split()
    word_counts = dict(pd.Series(words).value_counts())
    return word_counts

def read_word_file(file):
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def filter_keywords(text, keywords):
    keyword_lines = [line for line in text.split('\n') if any(keyword in line for keyword in keywords)]
    return keyword_lines

def filter_and_download(text, filter_type, keywords):
    if filter_type == 'custom':
        filtered_lines = filter_keywords(text, keywords)
        result_label = "### カスタム条件を満たす行のリスト"
        file_extension = "txt"
    else:
        st.error("無効なフィルタータイプが選択されました。")
        return

    if filtered_lines:
        result_text = "\n".join(filtered_lines)
        st.write(result_label)
        st.text(result_text)

        # Save the filtered lines to a text file
        file_name = f"{filter_type}_data.{file_extension}"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(result_text)

        st.download_button(label="テキストファイルとしてダウンロード", data=result_text, file_name=file_name, key=f"{filter_type}_download_button")
    else:
        st.write(f"テキストに対象の行は見つかりませんでした。")

def main():
    st.title("文章フィルター")

    uploaded_file = st.file_uploader("テキストファイルまたはワードファイルをアップロードしてください", type=["txt", "docx"])

    if uploaded_file is not None:
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = read_word_file(uploaded_file)
        else:
            text = uploaded_file.read().decode("utf-8")

        word_counts = count_words(text)
        result_df = pd.DataFrame(list(word_counts.items()), columns=['単語', '出現回数'])
        st.write("### 原本")
        st.dataframe(result_df)

        keywords = ['すべてのカタカナ', 'すべてのアルファベット', 'すべての数字']

        if st.button("カスタム条件を満たす文を抽出"):
            filter_and_download(text, 'custom', keywords)

if __name__ == "__main__":
    main()
