import streamlit as st
import pyttsx3
from pydub import AudioSegment

def main():
    st.title("Text-to-Speech with Streamlit")

    # Get user input
    voice_text = st.text_area("Enter the text you want to convert to speech", "米、大リーグ・エンゼルスの,大谷翔平投手は、13日（日本時間14日）、敵地、ガーディアンズ戦に、「3番・DH」で先発出場。左翼線に適時二塁打を放つなど、4打数、１安打、1打点、1四球だった。")

    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set engine properties
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)

    # Speak the entered text
    engine.say(voice_text)
    engine.runAndWait()

    # Save audio to a file
    prefix = voice_text[:4]
    output_file = f"{prefix}_output.mp3"
    engine.save_to_file(voice_text, output_file)

    # Display the audio file
    st.audio(output_file, format="audio/mp3", start_time=0)

if __name__ == "__main__":
    main()
