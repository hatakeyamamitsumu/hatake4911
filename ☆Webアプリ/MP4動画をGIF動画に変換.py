import streamlit as st
from moviepy.editor import VideoFileClip
from io import BytesIO

def convert_to_gif(video_path, fps=10):
    clip = VideoFileClip(video_path)
    
    # GIFをメモリに書き込む
    gif_buffer = BytesIO()
    clip.write_gif(gif_buffer, fps=fps)

    return gif_buffer

def main():
    st.title("MP4 to GIF Converter")

    # ファイルアップロード
    uploaded_file = st.file_uploader("Choose a MP4 file", type=["mp4"])

    if uploaded_file is not None:
        st.subheader("Options:")
        fps = st.slider("Select frames per second (FPS)", 1, 30, 10)

        st.subheader("Conversion:")
        st.write("Click the button below to convert the MP4 file to GIF.")
        if st.button("Convert to GIF"):
            # ファイルの変換
            gif_buffer = convert_to_gif(uploaded_file, fps)

            # 生成されたGIFの表示
            st.subheader("Converted GIF:")
            st.image(gif_buffer, use_column_width=True, format="GIF")

            # ダウンロードボタンの追加
            st.subheader("Download Converted GIF:")
            st.download_button(
                label="Download",
                data=gif_buffer.getvalue(),
                file_name="converted.gif",
                mime="image/gif",
            )

if __name__ == "__main__":
    main()
