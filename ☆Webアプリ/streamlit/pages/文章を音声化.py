import streamlit as st
import pyttsx3

def main():
    st.title("Text-to-Speech with Streamlit")

    # Get user input
    voice_text = st.text_area("Enter the text you want to convert to speech", "こんにちは、これはStreamlitを使用して文章を音声化するデモです。")

    # Initialize the text-to-speech engine with the 'sapi5' driver
    engine = pyttsx3.init(driverName='sapi5')

    # Set engine properties
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # voices[0]は日本語。voices[1]は英語、らしい
    engine.setProperty('rate', 180)

    # Speak the entered text
    engine.say(voice_text)
    engine.runAndWait()

if __name__ == "__main__":
    main()

