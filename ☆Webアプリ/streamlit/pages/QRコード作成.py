import streamlit as st
import qrcode
from PIL import Image
import io

# ユーザーにデータを入力させる
data = st.text_input("QRコードにしたい文字列を入力してください:")

# データが入力されていればQRコードを作成
if data:
    # QRコードを作成
    qr_img = qrcode.make(data)
    
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
        data=img_byte_array,  # QRコードのバイナリデータを指定
        key="download_qr_button",
        file_name="QR.png",  # ダウンロード時のファイル名を指定
    )
else:
    st.warning("データが入力されていません。QRコードにしたい文字列を入力してください。")

