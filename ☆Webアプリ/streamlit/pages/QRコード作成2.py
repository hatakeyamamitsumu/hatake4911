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

data = st.text_input("QRコードにしたい文字列を入力してください。URL以外の文字列でも大丈夫です")
qr_size = st.slider("QRコードの余白を調整してください", min_value=100, max_value=1000, value=500)
custom_text = st.text_input("QRコードに添える説明書き(アルファベットと数字のみ)")

# Add file name input field
file_name = st.text_input("QRコードのファイル名を入力してください", value="QR_code")

if data:
    try:
        qr_img = generate_qr_code(data, size=qr_size)
        if custom_text:
            qr_img = add_text_to_qr(qr_img, custom_text)

        img_byte_array = io.BytesIO()
        qr_img.save(img_byte_array, format='PNG')
        img_byte_array = img_byte_array.getvalue()

        img = Image.open(io.BytesIO(img_byte_array))
        st.image(img)

        # Use the provided file name input field
        st.download_button(
            label="QRコードをダウンロード",
            data=img_byte_array,
            key="download_qr_button",
            file_name=f"{file_name}.png",  # Use the provided file name
        )
    except Exception as e:
        st.error(f"QRコードの生成中にエラーが発生しました: {str(e)}")
else:
    st.warning("文字列を入力してください。")
