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

def filter_katakana(text):
    katakana_lines = [line for line in text.split('\n') if any('\u30A1' <= char <= '\u30F6' for char in line)]
    return katakana_lines

def filter_alphabets(text):
    alphabet_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ")
    alphabet_lines = [line for line in text.split('\n') if any(char in alphabet_characters for char in line)]
    return alphabet_lines

def filter_katakana_and_alphabets(text):
    katakana_and_alphabet_lines = [line for line in text.split('\n') if any('\u30A1' <= char <= '\u30F6' or char.isalpha() for char in line)]
    return katakana_and_alphabet_lines

def filter_and_download(text, filter_type):
    if filter_type == 'katakana':
        filtered_lines = filter_katakana(text)
        result_label = "### カタカナを含む行のリスト"
        file_extension = "txt"
    elif filter_type == 'alphabets':
        filtered_lines = filter_alphabets(text)
        result_label = "### アルファベットを含む行のリスト"
        file_extension = "txt"
    elif filter_type == 'katakana_and_alphabets':
        filtered_lines = filter_katakana_and_alphabets(text)
        result_label = "### カタカナとアルファベットを含む行のリスト"
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

        if st.button("カタカナを含む文を抽出"):
            filter_and_download(text, 'katakana')

        if st.button("アルファベットを含む文を抽出"):
            filter_and_download(text, 'alphabets')

        if st.button("カタカナとアルファベットを含む文を抽出"):
            filter_and_download(text, 'katakana_and_alphabets')

if __name__ == "__main__":
    main()

