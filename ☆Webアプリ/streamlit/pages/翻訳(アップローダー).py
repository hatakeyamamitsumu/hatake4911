import streamlit as st
import deepl

st.title("DeepL Translate App with File Upload")

LANGUAGES = {"英語": "EN", "日本語": "JA", "中国語": "ZH", "ドイツ語": "DE"}

def deepl_translate(text, src_lang="JA", target_lang="EN"):
    translated_text = deepl.translate(
        source_language=src_lang, target_language=target_lang, text=text
    )
    return translated_text

def main():
    st.title("DeepL Translate by Streamlit")
    uploaded_file = st.file_uploader("ファイルをアップロードしてください", type=['txt'])

    if uploaded_file is not None:
        file_contents = uploaded_file.read()

        src_lang = st.selectbox("入力テキストの言語", options=list(LANGUAGES.keys()))
        target_lang = st.selectbox("翻訳後テキストの言語", options=list(LANGUAGES.keys()))

        if st.button("翻訳する"):
            translated_text = deepl_translate(file_contents.decode('utf-8'),
                                              src_lang=LANGUAGES[src_lang],
                                              target_lang=LANGUAGES[target_lang])
            st.text("翻訳結果:")
            st.text(translated_text)

            # 翻訳結果をダウンロードする
            st.markdown(get_download_link(translated_text, "翻訳結果.txt"), unsafe_allow_html=True)

def get_download_link(text, filename):
    """指定されたテキストをファイルとしてダウンロードするためのリンクを生成する関数"""
    href = f'<a href="data:text/plain;charset=utf-8,{text}" download="{filename}">Click here to download {filename}</a>'
    return href

if __name__ == "__main__":
    main()
