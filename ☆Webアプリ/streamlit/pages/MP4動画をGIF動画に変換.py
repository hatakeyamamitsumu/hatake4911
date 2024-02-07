import streamlit as st
from moviepy.editor import VideoFileClip
from io import BytesIO
import base64  # 追加

def convert_to_gif(input_video, output_gif, fps=10):
    clip = VideoFileClip(input_video)
    clip.write_gif(output_gif, fps=fps)

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
            # アップロードされたファイルの変換
            input_video_path = "temp.mp4"
            output_gif_path = "output.gif"
            uploaded_file.seek(0)  # ファイルの先頭に移動
            with open(input_video_path, "wb") as temp_file:
                temp_file.write(uploaded_file.read())

            convert_to_gif(input_video_path, output_gif_path, fps)

            # セッションストレージにGIFデータを保存
            gif_buffer = BytesIO()
            with open(output_gif_path, "rb") as gif_file:
                gif_buffer.write(gif_file.read())
            st.session_state["converted_gif"] = gif_buffer.getvalue()

            # 生成されたGIFの表示
            st.subheader("Converted GIF:")
            st.markdown(
                f'<img src="data:image/gif;base64,{base64.b64encode(st.session_state["converted_gif"]).decode()}" alt="gif">',
                unsafe_allow_html=True,
            )

            # ダウンロードボタンの追加
            st.subheader("Download Converted GIF:")
            if "converted_gif" in st.session_state:
                st.download_button(
                    label="Download",
                    data=st.session_state["converted_gif"],
                    file_name="converted.gif",
                    mime="image/gif",
                )

if __name__ == "__main__":
    main()

