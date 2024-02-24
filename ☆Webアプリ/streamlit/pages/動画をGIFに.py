import streamlit as st
import cv2
from PIL import Image

uploaded_video = st.file_uploader("Choose video", type=["mp4", "mov"])
frame_skip = 300  # 300フレームごとに表示

if uploaded_video is not None:
    # ユーザーがビデオをアップロードした場合のみ実行
    vid = uploaded_video.name
    with open(vid, mode="wb") as f:
        f.write(uploaded_video.read())  # ビデオをディスクに保存

    st.markdown(f"### Files - {vid}", unsafe_allow_html=True)  # ファイル名を表示

    vidcap = cv2.VideoCapture(vid)  # ディスクからビデオを読み込む
    cur_frame = 0
    success = True

    while success:
        success, frame = vidcap.read()  # 次のフレームを取得
        if cur_frame % frame_skip == 0:
            # 300フレームごとにのみ分析
            pil_img = Image.fromarray(frame)  # OpenCVフレームをPILイメージに変換
            st.image(pil_img)  # 画像を表示
        cur_frame += 1

    # ダウンロードボタンを追加
    st.markdown(f'<a href="{vid}" download>Download GIF</a>', unsafe_allow_html=True)

