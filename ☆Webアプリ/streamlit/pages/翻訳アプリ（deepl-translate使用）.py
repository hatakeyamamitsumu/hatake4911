import deepl
import streamlit as st

st.title("deepl-translateという、deeplライブラリの非公式パッケージを使った翻訳アプリです。")

link_str = "(https://youtu.be/cUGeHn5vdfU)"#参考にしたサイト
st.markdown(link_str, unsafe_allow_html=True)

LANGUAGES = {"英語": "EN", "日本語": "JA", "中国語": "ZH", "ドイツ語": "DE"}

def deepl_translate(text, src_lang="JA", target_lang="EN"):
    translated_text = deepl.translate(
        source_language=src_lang, target_language=target_lang, text=text
    )
    return translated_text

def main():
    st.title("Deepl by Streamlit")
    main_container = st.container()

    left_col, right_col = main_container.columns(2)

    # left area contents
    src_lang = left_col.selectbox(
        "入力テキストの言語",
        options=LANGUAGES,
    )
    input_text = left_col.text_area("テキストを入力してください。", height=500)

    # right area contents
    target_lang = right_col.selectbox(
        "翻訳後テキストの言語",
        options=LANGUAGES,
    )
    right_col.text_area(
        "翻訳後のtext",
        value=deepl_translate(
            input_text, src_lang=LANGUAGES[src_lang], target_lang=LANGUAGES[target_lang]
        ),
        height=500,
    )

if __name__ == "__main__":
    main()
