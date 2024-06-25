import streamlit as st
from gtts import gTTS
import os
import base64

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
        
        # 一時的に保存するファイルのパス
        temp_path = "temp_output.mp3"
        tts.save(temp_path)
        
        # 音声ファイルを読み込み、セッションストレージに保持
        with open(temp_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            st.session_state['audio_data'] = audio_bytes
        
        # 音声ファイルを再生
        st.audio(audio_bytes, format="audio/mp3")
        
        # ダウンロードリンクを提供
        b64 = base64.b64encode(audio_bytes).decode()
        href = f'<a href="data:audio/mp3;base64,{b64}" download="output.mp3">Download the audio file</a>' if language == "English" else f'<a href="data:audio/mp3;base64,{b64}" download="output.mp3">音声ファイルをダウンロード</a>'
        st.markdown(href, unsafe_allow_html=True)
        
        # 一時ファイルの削除
        os.remove(temp_path)
    else:
        st.warning("Please enter some text to convert." if language == "English" else "変換するテキストを入力してください。")

# サイドバーに情報を表示
st.sidebar.title("About")
st.sidebar.info("This is a simple Text to Speech app using Streamlit and gTTS." if language == "English" else "これはStreamlitとgTTSを使用したシンプルなテキスト音声化アプリです。")
