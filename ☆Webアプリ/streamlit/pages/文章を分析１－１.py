#/mount/src/hatake4911/☆Webアプリ//CSVファイル各種/ヒートマップ地図用CSV
import streamlit as st
import pandas as pd
from docx import Document

def read_word_file(file):
    doc = Document(file)
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    return text

def read_additional_words_from_csv(file_path):
    additional_words_df = pd.read_csv(file_path)
    additional_words = additional_words_df['単語'].tolist()
    return additional_words

def filter_and_download(text, filter_words, additional_words=[]):
    lines_with_words = [line for line in text.split('\n') if any(word.lower() in line.lower() for word in filter_words)]

    if additional_words:
        lines_with_words = [line for line in lines_with_words if any(add_word.lower() in line.lower() for add_word in additional_words)]

    if lines_with_words:
        # Extracting lines with only filter_words
        filtered_lines = [line for line in lines_with_words if all(word.lower() in line.lower() for word in filter_words)]

        if filtered_lines:
            result_df = pd.DataFrame({"行": filtered_lines})
            st.write(f"### '{', '.join(filter_words)}' のみを含む行のリスト (or条件)")
            st.dataframe(result_df)

            result_text = "\n".join(filtered_lines)
            file_name = "filtered_data.txt"
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(result_text)

            st.download_button(label="テキストファイルとしてダウンロード", data=result_text, file_name=file_name, key="download_button")
        else:
            st.write(f"テキストに '{', '.join(filter_words)}' のみを含む行は見つかりませんでした。")
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

        additional_words_file_path = "/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/文章分析用CSV/自然.csv"
        additional_words = read_additional_words_from_csv(additional_words_file_path)

        filter_words = additional_words  # 使用する単語を additional_words に設定

        if filter_words:
            filter_and_download(text, filter_words, additional_words)

if __name__ == "__main__":
    main()
