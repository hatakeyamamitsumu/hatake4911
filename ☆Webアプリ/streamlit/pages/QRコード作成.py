import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

def generate_qr_code(data, size=300):
    # QRコードを作成
    qr_img = qrcode.make(data)

    # PIL Imageに変換
    img = Image.new("RGB", (size, size), "white")
    qr_img = qr_img.convert("RGB")
    img.paste(qr_img)

    return img

# ユーザーにデータを入力させる
data = st.text_input("QRコードにしたい文字列を入力してください:")

# データが入力されていればQRコードを作成
if data:
    try:
        # QRコードを作成
        qr_img = generate_qr_code(data)

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
    st.warning("データが入力されていません。QRコードにしたい文字列を入力してください。")

