import streamlit as st
from transformers import MarianMTModel, MarianTokenizer

# Streamlitアプリのタイトル
st.title('English to Japanese Translator')

# テキスト入力ボックスを設置
input_text = st.text_input('Enter English text to translate', '')

# 翻訳ボタンを設置
if st.button('Translate'):
    if input_text:
        # MarianMTモデルとトークナイザーの読み込み
        model_name = 'Helsinki-NLP/opus-mt-en-ja'
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        
        # 英語から日本語への翻訳を実行
        inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
        translated_tokens = model.generate(inputs, max_length=512)
        translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        
        st.write('Japanese translation:')
        st.write(translated_text)
    else:
        st.warning('Please enter some text to translate.')
