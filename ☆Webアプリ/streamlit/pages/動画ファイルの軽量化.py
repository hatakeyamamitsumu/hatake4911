import streamlit as st
from moviepy.editor import VideoFileClip

def compress_video(input_path, output_path, bitrate='500k'):
    clip = VideoFileClip(input_path)
    compressed_clip = clip.resize(height=360).fx(vfx.speedx, 0.5)
    compressed_clip.write_videofile(output_path, codec="libx264", bitrate=bitrate)

st.title('動画圧縮ツール')

# 動画ファイルのアップロード
uploaded_file = st.file_uploader("動画ファイルをアップロードしてください", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    st.subheader("圧縮前の動画")
    st.video(uploaded_file)

    # 圧縮設定
    compression_options = st.sidebar.selectbox(
        "圧縮設定",
        ("低", "中", "高")
    )

    bitrate_dict = {"低": "500k", "中": "1000k", "高": "2000k"}
    selected_bitrate = bitrate_dict[compression_options]

    # 圧縮実行
    st.subheader("圧縮中...")
    compressed_file_path = "compressed_video.mp4"
    compress_video(uploaded_file, compressed_file_path, bitrate=selected_bitrate)

    # 圧縮後の動画を表示
    st.subheader("圧縮後の動画")
    st.video(compressed_file_path)

    # 圧縮後の動画をダウンロード
    st.download_button(
        label="圧縮後の動画をダウンロード",
        data=open(compressed_file_path, "rb").read(),
        key="download_compressed_video_button",
        file_name="compressed_video.mp4",
    )
