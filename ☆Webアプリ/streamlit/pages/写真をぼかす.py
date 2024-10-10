import streamlit as st
from PIL import Image, ImageFilter

def convert_image(img):
    # Convert the PIL image to bytes
    from io import BytesIO
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def main():
    st.title("画像全体をぼかすアプリ")

    uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])
    blur_radius = st.sidebar.slider("ぼかしの強さ (半径)", min_value=1, max_value=50, value=10)

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        col1, col2 = st.columns(2)

        col1.write("オリジナル画像 :camera:")
        col1.image(image)

        # 画像全体をぼかす
        blurred_image = image.filter(ImageFilter.GaussianBlur(blur_radius))

        col2.write("ぼかし画像 :wrench:")
        col2.image(blurred_image)

        st.markdown("\n")
        st.download_button(
            "ダウンロード", convert_image(blurred_image), "blurred_image.png", "image/png"
        )

if __name__ == "__main__":
    main()
