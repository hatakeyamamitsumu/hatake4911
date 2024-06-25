import streamlit as st
from gtts import gTTS
import os

# Streamlitのタイトル
st.title("テキスト音声化アプリ")

# ユーザーにテキストを入力させる
text = st.text_area("音声に変換したいテキストを入力してください:")

if st.button("音声に変換"):
    if text:
        # gTTSを使用してテキストを音声に変換
        tts = gTTS(text, lang='ja')
        
        # 音声ファイルの名前を指定
        tts.save("output.mp3")
        
        # 音声ファイルを再生
        audio_file = open("output.mp3", "rb")
        audio_bytes = audio_file.read()
        
        st.audio(audio_bytes, format="audio/mp3")
        
        # ダウンロードリンクを提供
        st.markdown(f"[音声ファイルをダウンロード](./output.mp3)", unsafe_allow_html=True)
    else:
        st.warning("変換するテキストを入力してください。")

# サイドバーに情報を表示
st.sidebar.title("About")
st.sidebar.info("これはStreamlitとgTTSを使用したシンプルなテキスト音声化アプリです。")
