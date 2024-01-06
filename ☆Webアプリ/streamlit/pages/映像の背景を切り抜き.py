import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

st.set_page_config(layout="wide", page_title="Video Background Remover")

st.write("## 動画の背景を切り抜き")
st.write(
    "背景を切り抜きたい動画を、左のウインドウからアップロードしてください＜＜"
)
st.sidebar.write("## Upload and download :gear:")

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB (you can adjust this)

# Download the fixed video
def convert_video(frames, fps, width, height):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter("fixed_video.mp4", fourcc, fps, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()

    with open("fixed_video.mp4", "rb") as f:
        video_bytes = f.read()

    return video_bytes

def fix_video(upload):
    video = cv2.VideoCapture(upload)
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frames = []

    while True:
        ret, frame = video.read()
        if not ret:
            break

        # ここに背景を切り抜く処理を追加
        # 例: fixed_frame = remove(frame)

        # 切り抜いたフレームをframesに追加
        frames.append(fixed_frame)

    video.release()

    # 新しい動画の作成
    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download fixed video", convert_video(frames, fps, width, height), "fixed_video.mp4", "video/mp4")


col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload a video", type=["mp4"])

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload a video smaller than 100MB.")
    else:
        fix_video(upload=my_upload)

