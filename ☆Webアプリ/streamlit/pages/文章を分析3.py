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

def filter_numbers(text):
    number_lines = [line for line in text.split('\n') if any(char.isdigit() or re.search('[零壱弐参伍拾一二三四五六七八九十百千万億兆]', char) for char in line)]
    return number_lines

def filter_alphabets(text):
    alphabet_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ")
    alphabet_lines = [line for line in text.split('\n') if any(char in alphabet_characters for char in line)]
    return alphabet_lines

def apply_conditions(lines, conditions):
    filtered_lines = lines.copy()

    for condition in conditions:
        if condition['type'] == 'and':
            filtered_lines = [line for line in filtered_lines if all(keyword in line for keyword in condition['keywords'])]
        elif condition['type'] == 'or':
            filtered_lines = [line for line in filtered_lines if any(keyword in line for keyword in condition['keywords'])]
        elif condition['type'] == 'not':
            filtered_lines = [line for line in filtered_lines if all(keyword not in line for keyword in condition['keywords'])]

    return filtered_lines

def filter_and_download(text, filter_type, conditions):
    if filter_type == 'katakana':
        filtered_lines = filter_katakana(text)
    elif filter_type == 'numbers':
        filtered_lines = filter_numbers(text)
    elif filter_type == 'alphabets':
        filtered_lines = filter_alphabets(text)
    else:
        st.error("無効なフィルタータイプが選択されました。")
        return

    filtered_lines = apply_conditions(filtered_lines, conditions)

    if filtered_lines:
        result_text = "\n".join(filtered_lines)
        st.write("### 結果")
        st.text(result_text)

        # Save the filtered lines to a text file
        file_name = f"{filter_type}_data.txt"
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

        conditions = []

        if st.checkbox("カタカナ条件を追加"):
            katakana_keywords = st.text_input("カタカナのキーワードを入力（スペースで区切ってください）")
            if katakana_keywords:
                conditions.append({'type': 'or', 'keywords': katakana_keywords.split()})

        if st.checkbox("数字条件を追加"):
            numbers_keywords = st.text_input("数字のキーワードを入力（スペースで区切ってください）")
            if numbers_keywords:
                conditions.append({'type': 'or', 'keywords': numbers_keywords.split()})

        if st.checkbox("アルファベット条件を追加"):
            alphabets_keywords = st.text_input("アルファベットのキーワードを入力（スペースで区切ってください）")
            if alphabets_keywords:
                conditions.append({'type': 'or', 'keywords': alphabets_keywords.split()})

        if conditions:
            if st.button("選択した条件でフィルタリング"):
                filter_and_download(text, 'custom', conditions)

if __name__ == "__main__":
    main()
