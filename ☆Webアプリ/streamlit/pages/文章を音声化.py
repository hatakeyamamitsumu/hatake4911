import streamlit as st
from gtts import gTTS
import os

def main():
    st.title("Text-to-Speech with Streamlit")

    # ユーザーの入力を取得
    voice_text = st.text_area("音声に変換したいテキストを入力してください", "こんにちは、これはStreamlitを使用して文章を音声化するデモです。")

    # gTTSオブジェクトを作成
    tts = gTTS(text=voice_text, lang='ja')

    # 音声をファイルに保存
    prefix = voice_text[:4]
    output_file = f"{prefix}_output.mp3"
    tts.save(output_file)

    # 音声ファイルを表示
    st.audio(output_file, format="audio/mp3", start_time=0)

if __name__ == "__main__":
    main()

