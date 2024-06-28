import streamlit as st
from transformers import pipeline
from pydub import AudioSegment
import io

# Whisperモデルのロード
@st.cache_resource
def load_model():
    return pipeline('automatic-speech-recognition', model='openai/whisper-base')

# 音声ファイルをテキストに変換
def transcribe_audio(file):
    audio = AudioSegment.from_file(file)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio_bytes = io.BytesIO()
    audio.export(audio_bytes, format='wav')
    audio_bytes.seek(0)

    recognizer = load_model()
    result = recognizer(audio_bytes)

    return result['text']

st.title("Whisper音声文字起こしアプリ")
st.write("音声ファイルをアップロードしてください（mp3, wav, m4a形式に対応）")

# 音声ファイルのアップロード
uploaded_file = st.file_uploader("音声ファイルを選択", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    
    if st.button("文字起こし開始"):
        with st.spinner("文字起こし中..."):
            transcription = transcribe_audio(uploaded_file)
            st.write("文字起こし結果:")
            st.text(transcription)

