import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

st.title('QRコードに背景をつけて、分かりやすく！')
st.write('何のQRコードか分かりやすくなります。')
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

def resize_image(image, target_width):
    w_percent = (target_width / float(image.size[0]))
    h_size = int((float(image.size[1]) * float(w_percent)))
    return image.resize((target_width, h_size), Image.ANTIALIAS)

def overlay_images(background, overlay, position):
    overlay = overlay.convert("RGBA")
    background.paste(overlay, position, overlay)

# アップロードされた画像
uploaded_image = st.file_uploader("QRコードの内容を説明するための画像をアップロードしてください", type=["jpg", "jpeg", "png"])

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

        if uploaded_image is not None:
            uploaded_img = Image.open(io.BytesIO(uploaded_image.read()))
            # Resize QR code to 50% of the width of the uploaded image
            qr_img_resized = resize_image(qr_img, int(uploaded_img.width * 0.4))
            # Calculate the position for pasting QR code onto the uploaded image
            position = ((uploaded_img.width - qr_img_resized.width) // 2, (uploaded_img.height - qr_img_resized.height) // 2)
            # Overlay the QR code onto the uploaded image
            overlay_images(uploaded_img, qr_img_resized, position)
            st.image(uploaded_img, caption="生成された画像", use_column_width=True)

            img_byte_array = io.BytesIO()
            uploaded_img.save(img_byte_array, format='PNG')
            img_byte_array = img_byte_array.getvalue()

            # Use the provided file name input field
            st.download_button(
                label="画像とQRコードをダウンロード",
                data=img_byte_array,
                key="download_image_qr_button",
                file_name=f"{file_name}.png",  # Use the provided file name
            )
        else:
            st.image(qr_img, caption="生成されたQRコード", use_column_width=True)

            img_byte_array = io.BytesIO()
            qr_img.save(img_byte_array, format='PNG')
            img_byte_array = img_byte_array.getvalue()

            # Use the provided file name input field
            st.download_button(
                label="QRコードをダウンロード",
                data=img_byte_array,
                key="download_qr_button",
                file_name=f"{file_name}.png",  # Use the provided file name
            )
    except Exception as e:
        st.error(f"画像またはQRコードの生成中にエラーが発生しました: {str(e)}")
else:
    st.warning("文字列を入力してください。")
