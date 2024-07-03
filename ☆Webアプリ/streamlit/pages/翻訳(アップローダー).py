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

if __name__ == "__main__":
    main()
