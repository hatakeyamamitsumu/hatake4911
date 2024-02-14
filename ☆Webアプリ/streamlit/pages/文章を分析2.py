import streamlit as st
import pandas as pd
from io import StringIO
from docx import Document

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

def filter_katakana(text):
    katakana_lines = [line for line in text.split('\n') if any('\u30A1' <= char <= '\u30F6' for char in line)]
    return katakana_lines

import re

def filter_numbers(text):
    number_lines = [line for line in text.split('\n') if any(char.isdigit() or re.search('[一二三四五六七八九十百千万億兆]', char) for char in line)]
    return number_lines


def filter_and_download(text, filter_type):
    if filter_type == 'katakana':
        filtered_lines = filter_katakana(text)
        result_label = "### カタカナを含む行のリスト"
        file_name = "katakana_data.csv"
    elif filter_type == 'numbers':
        filtered_lines = filter_numbers(text)
        result_label = "### 数字を含む行のリスト"
        file_name = "number_data.csv"
    else:
        st.error("無効なフィルタータイプが選択されました。")
        return

    if filtered_lines:
        result_df = pd.DataFrame({"行": filtered_lines})
        st.write(result_label)
        st.dataframe(result_df)

        csv_data = StringIO()
        result_df.to_csv(csv_data, index=False)
        st.download_button(label="CSVファイルとしてダウンロード", data=csv_data.getvalue(), file_name=file_name, key=f"{filter_type}_download_button")
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

        # カタカナをフィルタリングするボタン
        if st.button("カタカナをフィルタリングする"):
            filter_and_download(text, 'katakana')

        # 数字をフィルタリングするボタン
        if st.button("数字をフィルタリングする"):
            filter_and_download(text, 'numbers')

if __name__ == "__main__":
    main()

