import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

st.title('QRコード作成')

def generate_qr_code(data, size=500):
    qr_img = qrcode.make(data)
    img = Image.new("RGB", (size, size), "white")
    qr_img = qr_img.convert("RGB")
    img.paste(qr_img)
    return img

def add_text_to_qr(img, text):
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((10, 10), text, font=font, fill="black")
    return img

def concatenate_images(left_img, right_img):
    max_width = max(left_img.width, right_img.width)
    max_height = max(left_img.height, right_img.height)

    left_img = left_img.resize((max_width, max_height))
    right_img = right_img.resize((max_width, max_height))

    concatenated_img = Image.new('RGB', (left_img.width + right_img.width, max_height))
    concatenated_img.paste(left_img, (0, 0))
    concatenated_img.paste(right_img, (left_img.width, 0))

    return concatenated_img

data = st.text_input("QRコードにしたい文字列を入力してください。URL以外の文字列でも大丈夫です")
qr_size = st.slider("QRコードの余白を調整してください", min_value=100, max_value=1000, value=500)
custom_text = st.text_input("QRコードに添える説明書き(アルファベットと数字のみ)")

# Add file name input field
file_name = st.text_input("QRコードのファイル名を入力してください", value="QR_code")

# Image upload
uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if data:
    try:
        qr_img = generate_qr_code(data, size=qr_size)
        if custom_text:
            qr_img = add_text_to_qr(qr_img, custom_text)

        if uploaded_image is not None:
            uploaded_img = Image.open(uploaded_image)
            # Concatenate images preserving the aspect ratio
            final_img = concatenate_images(qr_img, uploaded_img)
        else:
            final_img = qr_img

        st.image(final_img)

        img_byte_array = io.BytesIO()
        final_img.save(img_byte_array, format='PNG')
        img_byte_array = img_byte_array.getvalue()

        # Use the provided file name input field
        st.download_button(
            label="QRコードをダウンロード",
            data=img_byte_array,
            key="download_qr_button",
            file_name=f"{file_name}.png",  # Use the provided file name
        )
    except Exception as e:
        st.error(f"QRコードの生成中または画像の結合中にエラーが発生しました: {str(e)}")
else:
    st.warning("文字列を入力してください。")
