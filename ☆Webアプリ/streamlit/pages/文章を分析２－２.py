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

def filter_katakana(text, filter_condition):
    katakana_lines = [line for line in text.split('\n') if any('\u30A1' <= char <= '\u30F6' for char in line)]
    return katakana_lines

import re

def filter_numbers(text, filter_condition):
    number_lines = [line for line in text.split('\n') if any(char.isdigit() or re.search('[零壱弐参伍拾一二三四五六七八九十百千万億兆]', char) for char in line)]
    return number_lines

def filter_alphabets(text, filter_condition):
    alphabet_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ")
    alphabet_lines = [line for line in text.split('\n') if any(char in alphabet_characters for char in line)]
    return alphabet_lines

def filter_and_download(text, filter_type, filter_condition):
    if filter_type == 'katakana':
        filtered_lines = filter_katakana(text, filter_condition)
        result_label = "### カタカナを含む行のリスト"
        file_name = "katakana_data.csv"
    elif filter_type == 'numbers':
        filtered_lines = filter_numbers(text, filter_condition)
        result_label = "### 数字（漢数字を含む）を含む行のリスト"
        file_name = "number_data.csv"
    elif filter_type == 'alphabets':
        filtered_lines = filter_alphabets(text, filter_condition)
        result_label = "### アルファベットを含む行のリスト"
        file_name = "alphabet_data.csv"
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

        filter_type = st.radio("フィルタータイプを選択してください:", ['katakana', 'numbers', 'alphabets'])
        filter_condition = st.radio("条件を選択してください:", ['and', 'or', 'not'])

        if st.button(f"{filter_type.capitalize()} を含む文を抽出"):
            filter_and_download(text, filter_type, filter_condition)

if __name__ == "__main__":
    main()
