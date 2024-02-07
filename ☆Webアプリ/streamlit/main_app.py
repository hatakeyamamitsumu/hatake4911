import streamlit as st
from moviepy.editor import VideoFileClip
from io import BytesIO

def convert_to_gif(video_file, fps=10):
    # .mp4 ファイルかどうか確認
    if video_file.name.endswith('.mp4'):
        # ファイルを一時的に保存
        with st.spinner("Converting..."):
            with open("temp.mp4", "wb") as temp_file:
                temp_file.write(video_file.read())
        
        # 動画をGIFに変換
        clip = VideoFileClip("temp.mp4")
        gif_buffer = BytesIO()
        clip.write_gif(gif_buffer, fps=fps)
        
        # 一時的に作成したファイルを削除
        st.experimental_rerun()
        return gif_buffer

    else:
        st.error("Please upload a valid .mp4 file.")
        return None

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

            if gif_buffer is not None:
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
