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

def apply_condition(lines, condition):
    if condition == 'and':
        return list(set.intersection(*map(set, lines)))
    elif condition == 'or':
        return list(set.union(*map(set, lines)))
    elif condition == 'not':
        return list(set(lines[0]) - set.intersection(*map(set, lines[1:])))

def filter_not_selected_conditions(text, selected_conditions):
    all_conditions = ['katakana', 'numbers', 'alphabets']
    conditions_to_exclude = set(all_conditions) - set(selected_conditions)

    excluded_lines = []
    for condition in conditions_to_exclude:
        if condition == 'katakana':
            excluded_lines.extend(filter_katakana(text))
        elif condition == 'numbers':
            excluded_lines.extend(filter_numbers(text))
        elif condition == 'alphabets':
            excluded_lines.extend(filter_alphabets(text))

    return list(set(text.split('\n')) - set(excluded_lines))

def filter_and_download(text, selected_conditions, condition_type):
    filtered_lines = []

    for condition in selected_conditions:
        if condition == 'katakana':
            filtered_lines.append(filter_katakana(text))
        elif condition == 'numbers':
            filtered_lines.append(filter_numbers(text))
        elif condition == 'alphabets':
            filtered_lines.append(filter_alphabets(text))

    if filtered_lines:
        if condition_type == 'and':
            result_lines = apply_condition(filtered_lines, condition_type)
        elif condition_type == 'or':
            result_lines = apply_condition(filtered_lines, condition_type)
        elif condition_type == 'not':
            result_lines = filter_not_selected_conditions(text, selected_conditions)
        else:
            st.error("無効な条件の種類が選択されました。")
            return

        if result_lines:
            result_label = "### 結果"
            result_text = "\n".join(result_lines)

            st.write(result_label)
            st.text(result_text)

            # Save the filtered lines to a text file
            file_name = f"filtered_data.txt"
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(result_text)

            st.download_button(label="テキストファイルとしてダウンロード", data=result_text, file_name=file_name, key=f"filtered_download_button")
        else:
            st.write(f"条件に合致する行が見つかりませんでした。")
    else:
        st.write("無効な条件が選択されました。")

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

        selected_conditions = st.multiselect("条件を選択してください", ['katakana', 'numbers', 'alphabets'])

        condition_type = st.selectbox("条件の種類を選択してください", ['and', 'or', 'not'])

        if st.button("条件に基づいて文を抽出"):
            filter_and_download(text, selected_conditions, condition_type)

if __name__ == "__main__":
    main()
