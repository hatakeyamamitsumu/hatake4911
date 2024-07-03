import streamlit as st
import deepl

st.title("Deepl Translate App with File Upload")

LANGUAGES = {"英語": "EN", "日本語": "JA", "中国語": "ZH", "ドイツ語": "DE"}

def deepl_translate(text, src_lang="JA", target_lang="EN"):
    # 文章を適当な長さに分割して、翻訳を実行
    chunk_size = 5000  # 適当な文章の長さ
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    translated_chunks = []
    for chunk in chunks:
        translated_text = deepl.translate(
            source_language=src_lang, target_language=target_lang, text=chunk
        )
        translated_chunks.append(translated_text)
    
    # 翻訳された各チャンクを連結して最終的な翻訳結果を返す
    return " ".join(translated_chunks)

def main():
    st.title("Deepl Translate by Streamlit")
    uploaded_file = st.file_uploader("ファイルをアップロードしてください", type=['txt'])

    if uploaded_file is not None:
        file_contents = uploaded_file.read().decode('utf-8')

        src_lang = st.selectbox("入力テキストの言語", options=list(LANGUAGES.keys()))
        target_lang = st.selectbox("翻訳後テキストの言語", options=list(LANGUAGES.keys()))

        if st.button("翻訳する"):
            translated_text = deepl_translate(file_contents,
                                              src_lang=LANGUAGES[src_lang],
                                              target_lang=LANGUAGES[target_lang])
            st.text("翻訳結果:")
            st.text(translated_text)

            # 翻訳結果をダウンロードするリンクを表示
            st.markdown(get_download_link(translated_text, "translated_text.txt"), unsafe_allow_html=True)

def get_download_link(text, filename):
    # テキストをファイルとしてダウンロードするリンクを生成する関数
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">ここをクリックしてダウンロード</a>'
    return href

if __name__ == "__main__":
    main()
