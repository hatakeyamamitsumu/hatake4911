import streamlit as st
import pandas as pd
from io import StringIO
from docx import Document

def count_words(text):
    # テキストから単語を抽出してカウント
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
    # 行のフィルタリング
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
        # 結果をデータフレームに変換
        result_df = pd.DataFrame({"行": lines_with_words})

        # 結果を表示
        st.write(f"### '{', '.join(filter_words)}' を含む行のリスト ({filter_condition} 条件)")
        st.dataframe(result_df)

        # 結果をCSVファイルとしてダウンロード
        csv_data = StringIO()
        result_df.to_csv(csv_data, index=False)
        st.download_button(label="CSVファイルとしてダウンロード", data=csv_data.getvalue(), file_name="filtered_data.csv", key="download_button")
    else:
        st.write(f"テキストに '{', '.join(filter_words)}' を含む行は見つかりませんでした。")

def main():
    st.title("文章フィルター")

    # ファイルアップロード
    uploaded_file = st.file_uploader("テキストファイルまたはワードファイルをアップロードしてください", type=["txt", "docx"])

    if uploaded_file is not None:
        # アップロードされたファイルを読み込む
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = read_word_file(uploaded_file)
        else:
            text = uploaded_file.read().decode("utf-8")

        # 単語出現回数をカウント
        word_counts = count_words(text)

        # 結果をデータフレームに変換
        result_df = pd.DataFrame(list(word_counts.items()), columns=['単語', '出現回数'])

        # 結果を表示
        st.write("### 原本")
        st.dataframe(result_df)

        # フィルタリングする単語を入力
        filter_words = st.text_area("フィルタリングする単語をスペースで区切って入力してください:")
        
        # 条件を選択
        filter_condition = st.radio("条件を選択してください:", ['and', 'or', 'not'])

        if filter_words:
            filter_words = filter_words.split()
            filter_and_download(text, filter_words, filter_condition)

if __name__ == "__main__":
    main()
