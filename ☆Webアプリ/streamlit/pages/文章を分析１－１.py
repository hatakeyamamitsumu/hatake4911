
#/mount/src/hatake4911/☆Webアプリ//CSVファイル各種/ヒートマップ地図用CSV
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

def read_additional_words_from_csv(file_path):
    additional_words_df = pd.read_csv(file_path)
    additional_words = additional_words_df['単語'].tolist()
    return additional_words

def filter_and_download(text, filter_words, filter_condition, additional_words=[]):
    if filter_condition == 'and':
        lines_with_words = [line for line in text.split('\n') if all(word.lower() in line.lower() for word in filter_words)]
    elif filter_condition == 'or':
        lines_with_words = [line for line in text.split('\n') if any(word.lower() in line.lower() for word in filter_words)]
    elif filter_condition == 'not':
        lines_with_words = [line for line in text.split('\n') if all(word.lower() not in line.lower() for word in filter_words)]
    else:
        st.error("無効な条件が選択されました。'and', 'or', または 'not' を選択してください。")
        return

    if additional_words:
        lines_with_words = [line for line in lines_with_words if any(add_word.lower() in line.lower() for add_word in additional_words)]

    if lines_with_words:
        result_df = pd.DataFrame({"行": lines_with_words})
        st.write(f"### '{', '.join(filter_words + additional_words)}' を含む行のリスト ({filter_condition} 条件)")
        st.dataframe(result_df)

        result_text = "\n".join(lines_with_words)
        file_name = "filtered_data.txt"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(result_text)

        st.download_button(label="テキストファイルとしてダウンロード", data=result_text, file_name=file_name, key="download_button")
    else:
        st.write(f"テキストに '{', '.join(filter_words + additional_words)}' を含む行は見つかりませんでした。")

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

        additional_words_file_path = "/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/文章分析用CSV/自然.csv"
        additional_words = read_additional_words_from_csv(additional_words_file_path)

        filter_condition = st.radio("条件を選択してください:", ['and', 'or', 'not'])

        if additional_words:
            filter_and_download(text, additional_words, filter_condition, additional_words)

if __name__ == "__main__":
    main()
