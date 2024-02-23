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

def filter_all_katakana(text):
    all_katakana_lines = [line for line in text.split('\n') if all('\u30A1' <= char <= '\u30F6' for char in line)]
    return all_katakana_lines

def filter_all_alphabets(text):
    all_alphabet_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ")
    all_alphabet_lines = [line for line in text.split('\n') if all(char in all_alphabet_characters for char in line)]
    return all_alphabet_lines

def filter_and_download(text, filter_type):
    if filter_type == 'all_katakana':
        filtered_lines = filter_all_katakana(text)
        result_label = "### 全てのカタカナを含む行のリスト"
        file_extension = "txt"
    elif filter_type == 'all_alphabets':
        filtered_lines = filter_all_alphabets(text)
        result_label = "### 全てのアルファベットを含む行のリスト"
        file_extension = "txt"
    elif filter_type == 'katakana_or_alphabets':
        katakana_lines = filter_all_katakana(text)
        alphabet_lines = filter_all_alphabets(text)
        filtered_lines = katakana_lines + alphabet_lines
        result_label = "### 全てのカタカナ or 全てのアルファベットを含む行のリスト"
        file_extension = "txt"
    elif filter_type == 'katakana_and_alphabets':
        katakana_lines = filter_all_katakana(text)
        alphabet_lines = filter_all_alphabets(text)
        filtered_lines = list(set(katakana_lines) & set(alphabet_lines))
        result_label = "### 全てのカタカナ and 全てのアルファベットを含む行のリスト"
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

        if st.button("全てのカタカナを含む文を抽出"):
            filter_and_download(text, 'all_katakana')

        if st.button("全てのアルファベットを含む文を抽出"):
            filter_and_download(text, 'all_alphabets')

        if st.button("全てのカタカナ or 全てのアルファベットを含む文を抽出"):
            filter_and_download(text, 'katakana_or_alphabets')

        if st.button("全てのカタカナ and 全てのアルファベットを含む文を抽出"):
            filter_and_download(text, 'katakana_and_alphabets')

if __name__ == "__main__":
    main()
