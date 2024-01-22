import streamlit as st
import qrcode
from PIL import Image
import io
import numpy as np
# ユーザーにデータを入力させる
data = st.text_input("QRコードにしたい文字列を入力してください:")

# データが入力されていればQRコードを作成
if data:
    # QRコードを作成
    _qr_img = qrcode.make(data)
    # 画像をファイルとして保存
    _qr_img.save("QR.png")
    img=Image.open("QR.png")
    st.image(img)



    # ダウンロードボタンを表示
    st.download_button(
        label="QRコードをダウンロード",
        data="QR.png",
        key="download_qr_button"
    )
else:
    st.warning("データが入力されていません。QRコードにしたい文字列を入力してください。")

