import streamlit as st
from gtts import gTTS
import os

# Streamlitのタイトル
st.title("Text to Speech App / テキスト音声化アプリ")

# ユーザーに言語を選択させる
language = st.selectbox("Choose language / 言語を選択してください", ("English", "日本語"))

# ユーザーにテキストを入力させる
if language == "English":
    text = st.text_area("Enter the text you want to convert to speech:")
else:
    text = st.text_area("音声に変換したいテキストを入力してください:")

if st.button("Convert to Speech" if language == "English" else "音声に変換"):
    if text:
        # gTTSを使用してテキストを音声に変換
        lang_code = 'en' if language == "English" else 'ja'
        tts = gTTS(text, lang=lang_code)
        
        # 音声ファイルの名前とパスを指定
        output_path = "output.mp3"
        tts.save(output_path)
        
        # 音声ファイルを再生
        audio_file = open(output_path, "rb")
        audio_bytes = audio_file.read()
        
        st.audio(audio_bytes, format="audio/mp3")
        
        # ダウンロードリンクを提供
        st.markdown(f"[Download the audio file](output.mp3)" if language == "English" else f"[音声ファイルをダウンロード](output.mp3)", unsafe_allow_html=True)
    else:
        st.warning("Please enter some text to convert." if language == "English" else "変換するテキストを入力してください。")

# サイドバーに情報を表示
st.sidebar.title("About")
st.sidebar.info("This is a simple Text to Speech app using Streamlit and gTTS." if language == "English" else "これはStreamlitとgTTSを使用したシンプルなテキスト音声化アプリです。")
