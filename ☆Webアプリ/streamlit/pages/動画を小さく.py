import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_resize

# Streamlitの設定
st.title("動画圧縮アプリ")
st.write("アップロードした動画のファイルサイズを小さくします。")

# 動画のアップロード
uploaded_file = st.file_uploader("動画をアップロードしてください", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    # 動画ファイルを一時ファイルに保存
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    # 動画をMoviePyで読み込む
    video = VideoFileClip(tfile.name)
    
    # 動画の解像度を設定
    resolution = st.slider("解像度 (幅)", 160, video.size[0], video.size[0]//2)
    height = int(video.size[1] * resolution / video.size[0])
    
    # ビットレートの設定
    bitrate = st.slider("ビットレート (kbps)", 100, 5000, 1000)
    
    # 圧縮実行ボタン
    if st.button("圧縮を実行"):
        # 圧縮中の進捗バー
        progress_bar = st.progress(0)
        
    def update_progress_callback(progress, *args):
        progress_bar.progress(progress)


        # 圧縮後の動画を一時ファイルに保存
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        video_resized = video.resize((resolution, height))
        
        # 動画を圧縮する
        video_resized.write_videofile(
            output_path,
            bitrate=f"{bitrate}k",
            logger=None,
            verbose=False,
            progress_bar=True,
            progress_callback=update_progress_callback
        )
        
        # 圧縮後のファイルサイズを表示
        size_before = os.path.getsize(tfile.name)
        size_after = os.path.getsize(output_path)
        st.write(f"圧縮前のファイルサイズ: {size_before / (1024*1024):.2f} MB")
        st.write(f"圧縮後のファイルサイズ: {size_after / (1024*1024):.2f} MB")
        
        # 圧縮後の動画をダウンロードリンクとして提供
        with open(output_path, "rb") as file:
            st.download_button(
                label="圧縮された動画をダウンロード",
                data=file,
                file_name="compressed_video.mp4",
                mime="video/mp4"
            )
        
        # 一時ファイルの削除
        os.remove(tfile.name)
        os.remove(output_path)
