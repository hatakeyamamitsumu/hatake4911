import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

def generate_customized_qr_code(data, color="black", background_color="white", size=300):
    # QRコードを作成
    qr_img = qrcode.make(data)

    # PIL Imageに変換
    img = Image.new("RGB", (size, size), background_color)
    qr_img = qr_img.convert("RGB")
    img.paste(qr_img)

    # QRコードのデザインをカスタマイズ（例：色を変更）
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((10, 10), data, font=font, fill=color)

    return img

# ユーザーにデータを入力させる
data = st.text_input("QRコードにしたい文字列を入力してください:")

# カスタマイズオプションを追加
color = st.color_picker("QRコードの色を選択してください", "#000000")
background_color = st.color_picker("背景色を選択してください", "#FFFFFF")
size = st.slider("QRコードのサイズを調整してください", min_value=100, max_value=500, value=300)

# データが入力されていればQRコードを作成
if data:
    try:
        # カスタマイズされたQRコードを作成
        qr_img = generate_customized_qr_code(data, color, background_color, size)

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
