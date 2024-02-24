import streamlit as st
from moviepy.editor import VideoFileClip
from io import BytesIO
import os

def resize_and_change_framerate(input_file, new_fps, scale_factor):
    # ファイルを一時的に保存
    with open("temp_video.mp4", "wb") as temp_file:
        temp_file.write(input_file.read())

    # 入力動画の読み込み
    clip = VideoFileClip("temp_video.mp4")
    
    # フレームレートを変更
    clip = clip.set_fps(new_fps)
    
    # サイズを変更
    new_size = tuple(int(dim * scale_factor) for dim in clip.size)
    clip = clip.resize(new_size)
    
    # 一時ファイルを削除
    os.remove("temp_video.mp4")

    return clip

def main():
    st.title("動画リサイズ＆フレームレート変更アプリ")

    # 動画ファイルのアップロード
    uploaded_file = st.file_uploader("動画ファイルをアップロードしてください", type=["mp4"])

    if uploaded_file is not None:
        new_fps = st.slider("新しいフレームレート", min_value=1, max_value=60, value=30)
        scale_factor = st.slider("サイズを変更する割合", min_value=0.1, max_value=2.0, value=0.8, step=0.1)

        # 動画処理
        processed_clip = resize_and_change_framerate(uploaded_file, new_fps, scale_factor)

        # 出力ファイル名
        output_filename = f"output_{new_fps}fps_{int(scale_factor*100)}percent.mp4"

        # 出力動画を表示
        st.video(processed_clip, format="mp4")

        # ダウンロードボタン
        with st.beta_expander("動画をダウンロード"):
            buffer = BytesIO()
            processed_clip.write_videofile(buffer, codec="libx264", audio_codec="aac")
            st.download_button("ダウンロード", file_content=buffer.getvalue(), file_name=output_filename, key='download_button')

if __name__ == "__main__":
    main()
