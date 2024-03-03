import streamlit as st
import pandas as pd
from io import StringIO
from docx import Document

def count_words(text):
    # Extract words from text and count occurrences
    words = text.split()
    word_counts = dict(pd.Series(words).value_counts())
    return word_counts

def read_word_file(file):
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def filter_and_download(text, filter_words, filter_condition):
    # Filtering lines based on conditions
    if filter_condition == 'and':
        lines_with_words = [line for line in text.split('\n') if all(word.lower() in line.lower() for word in filter_words)]
    elif filter_condition == 'or':
        lines_with_words = [line for line in text.split('\n') if any(word.lower() in line.lower() for word in filter_words)]
    elif filter_condition == 'not':
        lines_with_words = [line for line in text.split('\n') if all(word.lower() not in line.lower() for word in filter_words)]
    else:
        st.error("無効な条件が選択されました。'and', 'or', または 'not' を選択してください。")
        return

    if lines_with_words:
        # Convert results to a DataFrame
        result_df = pd.DataFrame({"行": lines_with_words})

        # Display results
        st.write(f"### '{', '.join(filter_words)}' を含む行のリスト ({filter_condition} 条件)")
        st.dataframe(result_df)

        # Save the filtered lines to a text file
        result_text = "\n".join(lines_with_words)
        file_name = "filtered_data.txt"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(result_text)

        st.download_button(label="テキストファイルとしてダウンロード", data=result_text, file_name=file_name, key="download_button")
    else:
        st.write(f"テキストに '{', '.join(filter_words)}' を含む行は見つかりませんでした。")

def main():
    st.title("テキストから文章を抽出")
    st.write("複数の単語を入力し、その語が含まれる行を抽出するアプリです。特定の文脈の内容をざっくりと抽出するときにご利用ください。")

    # File upload
    uploaded_file = st.file_uploader("テキストファイルまたはワードファイルをアップロードしてください", type=["txt", "docx"])

    if uploaded_file is not None:
        # Read the uploaded file
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = read_word_file(uploaded_file)
        else:
            text = uploaded_file.read().decode("utf-8")

        # Count word occurrences
        word_counts = count_words(text)

        # Convert results to a DataFrame
        result_df = pd.DataFrame(list(word_counts.items()), columns=['単語', '出現回数'])

        # Display results
        st.write("### 原本")
        st.dataframe(result_df)

        # Input words to filter
        filter_words = st.text_area("フィルタリングする単語をスペースで区切って入力してください:")
        
        # Choose filtering condition
        filter_condition = st.radio("条件を選択してください:", ['and', 'or', 'not'])

        if filter_words:
            filter_words = filter_words.split()
            filter_and_download(text, filter_words, filter_condition)

if __name__ == "__main__":
    main()

