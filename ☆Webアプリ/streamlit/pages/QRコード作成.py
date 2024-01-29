import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

def generate_qr_code(data, size=500):
    # QRコードを作成
    qr_img = qrcode.make(data)

    # PIL Imageに変換
    img = Image.new("RGB", (size, size), "white")
    qr_img = qr_img.convert("RGB")
    img.paste(qr_img)

    return img

def add_text_to_qr(img, text):
    # 画像にテキストを追加
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((10, 10), text, font=font, fill="black")

    return img

# ユーザーにデータを入力させ、QRコードのサイズとテキストを調節可能にする
data = st.text_input("QRコードにする文字列を入力してください")
qr_size = st.slider("QRコードの余白を調整してください", min_value=100, max_value=1000, value=500)
custom_text = st.text_input("QRコードに添える説明書き(アルファベットと数字のみ)")

# データが入力されていればQRコードを作成
if data:
    try:
        # QRコードを作成
        qr_img = generate_qr_code(data, size=qr_size)

        # ユーザーがテキストを入力していれば、QRコードにテキストを追加
        if custom_text:
            qr_img = add_text_to_qr(qr_img, custom_text)

        # 画像をファイルとして保存
        img_byte_array = io.BytesIO()
        qr_img.save(img_byte_array, format='PNG')
        img_byte_array = img_byte_array.getvalue()

        # Streamlitで画像を表示
        img = Image.open(io.BytesIO(img_byte_array))
        st.image(img)

        # ダウンロードボタンを表示
        st.download_button(
            label="QRコードをダウンロード",
            data=img_byte_array,
            key="download_qr_button",
            file_name="QR.png",
        )
    except Exception as e:
        st.error(f"QRコードの生成中にエラーが発生しました: {str(e)}")
else:
    st.warning("QRコードにしたい文字列を入力してください。URL以外の文字列でも大丈夫です")
