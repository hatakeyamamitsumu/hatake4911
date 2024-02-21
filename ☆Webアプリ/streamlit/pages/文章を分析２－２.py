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

def filter_katakana(text, filter_condition):
    katakana_lines = [line for line in text.split('\n') if any('\u30A1' <= char <= '\u30F6' for char in line)]
    return katakana_lines

def filter_numbers(text, filter_condition):
    number_lines = [line for line in text.split('\n') if any(char.isdigit() or re.search('[零壱弐参伍拾一二三四五六七八九十百千万億兆]', char) for char in line)]
    return number_lines

def filter_alphabets(text, filter_condition):
    alphabet_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ")
    alphabet_lines = [line for line in text.split('\n') if any(char in alphabet_characters for char in line)]
    return alphabet_lines

def filter_and_download(text, filter_condition_katakana, filter_condition_numbers, filter_condition_alphabets):
    katakana_lines = filter_katakana(text, filter_condition_katakana)
    number_lines = filter_numbers(text, filter_condition_numbers)
    alphabet_lines = filter_alphabets(text, filter_condition_alphabets)

    if filter_condition == 'and':
        filtered_lines = list(set(katakana_lines) & set(number_lines) & set(alphabet_lines))
    elif filter_condition == 'or':
        filtered_lines = list(set(katakana_lines) | set(number_lines) | set(alphabet_lines))
    elif filter_condition == 'not':
        filtered_lines = list(set(katakana_lines) - set(number_lines) - set(alphabet_lines))
    else:
        st.error("無効な条件が選択されました。'and', 'or', または 'not' を選択してください。")
        return

    if filtered_lines:
        result_df = pd.DataFrame({"行": filtered_lines})
        st.write(f"### カタカナ、アルファベット、数字を含む行のリスト ({filter_condition} 条件)")
        st.dataframe(result_df)

        csv_data = StringIO()
        result_df.to_csv(csv_data, index=False)
        st.download_button(label="CSVファイルとしてダウンロード", data=csv_data.getvalue(), file_name="filtered_data.csv", key="download_button")
    else:
        st.write("指定した条件に一致する行は見つかりませんでした。")

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

        filter_condition_katakana = st.radio("カタカナの条件を選択してください:", ['and', 'or', 'not'])
        filter_condition_numbers = st.radio("数字（漢数字を含む）の条件を選択してください:", ['and', 'or', 'not'])
        filter_condition_alphabets = st.radio("アルファベットの条件を選択してください:", ['and', 'or', 'not'])

        if st.button("条件に一致する行を抽出"):
            filter_and_download(text, filter_condition_katakana, filter_condition_numbers, filter_condition_alphabets)

if __name__ == "__main__":
    main()
