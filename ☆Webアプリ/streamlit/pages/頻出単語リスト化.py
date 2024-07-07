import streamlit as st
from collections import Counter
import string
import pandas as pd
from io import StringIO
import base64  # Add this import

def calculate_word_frequency(text):
    # 文字句の前処理
    text = text.lower()  # 小文字に変換
    text = text.translate(str.maketrans('', '', string.punctuation))  # 句読点を除去

    # 単語ごとに分割して頻度をカウント
    words = text.split()
    word_freq = Counter(words)

    return word_freq

def main():
    st.title('文章の単語頻出度チェッカー')
    st.write('テキストファイルをアップロードしてください。')

    uploaded_file = st.file_uploader("テキストファイルを選択", type=['txt'])

    if uploaded_file is not None:
        # ファイル内容を読み込む
        text = uploaded_file.read().decode('utf-8')

        # 単語頻度を計算
        word_freq = calculate_word_frequency(text)

        # 単語頻度を昇順にソート
        sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1])

        # 結果を表示
        st.header('単語の頻出度（昇順）')
        for word, freq in sorted_word_freq:
            st.write(f"- {word}: {freq}")

        # ダウンロードボタンを追加
        df = pd.DataFrame(sorted_word_freq, columns=['単語', '頻出度'])
        csv = df.to_csv(index=False, encoding='utf-8')
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="word_frequencies.csv">ダウンロードCSVファイル</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
