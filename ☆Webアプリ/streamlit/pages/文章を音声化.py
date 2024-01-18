import streamlit as st
from gtts import gTTS
import os

def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False)
    audio_file = 'output.mp3'
    tts.save(audio_file)
    return audio_file

def main():
    st.title("Text to Speech App")

    # テキスト入力
    text_input = st.text_area("Enter text to convert to speech", "Hello, this is Streamlit!")

    # 言語の選択
    language = st.selectbox("Select language", ["en", "ja"])

    # 変換ボタン
    if st.button("Convert to Speech"):
        st.write("Converting...")
        audio_file = text_to_speech(text_input, language)
        st.audio(audio_file, format='audio/mp3', start_time=0)
        st.success("Conversion complete!")

        # 生成した音声ファイルを削除
        os.remove(audio_file)

if __name__ == "__main__":
    main()
