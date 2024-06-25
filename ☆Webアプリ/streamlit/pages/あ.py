import streamlit as st
from gtts import gTTS
import os

# Streamlitのタイトル
st.title("Text to Speech App")

# ユーザーにテキストを入力させる
text = st.text_area("Enter the text you want to convert to speech:")

if st.button("Convert to Speech"):
    if text:
        # gTTSを使用してテキストを音声に変換
        tts = gTTS(text)
        
        # 音声ファイルの名前を指定
        tts.save("output.mp3")
        
        # 音声ファイルを再生
        audio_file = open("output.mp3", "rb")
        audio_bytes = audio_file.read()
        
        st.audio(audio_bytes, format="audio/mp3")
        
        # ダウンロードリンクを提供
        st.markdown(f"[Download the audio file](./output.mp3)", unsafe_allow_html=True)
    else:
        st.warning("Please enter some text to convert.")

# サイドバーに情報を表示
st.sidebar.title("About")
st.sidebar.info("This is a simple Text to Speech app using Streamlit and gTTS.")
