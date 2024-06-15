import streamlit as st
from translate import Translator

# Streamlitアプリのタイトル
st.title('English to Japanese Translator')

# テキスト入力ボックスを設置
input_text = st.text_input('Enter English text to translate', '')

# 翻訳ボタンを設置
if st.button('Translate'):
    if input_text:
        # 英語から日本語への翻訳を実行
        translator = Translator(to_lang="ja")
        translated_text = translator.translate(input_text)
        st.write('Japanese translation:')
        st.write(translated_text)
    else:
        st.warning('Please enter some text to translate.')
