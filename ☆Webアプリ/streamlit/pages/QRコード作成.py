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

    # Streamlitで画像を表示
    st.image(qr_img, caption='QR Code', use_column_width=True)

    # 画像をファイルとして保存
    qr_img.save("QR.png")

    # ダウンロードボタンを表示
    st.download_button(
        label="QRコードをダウンロード",
        data="QR.png",
        key="download_qr_button"
    )
else:
    st.warning("データが入力されていません。QRコードにしたい文字列を入力してください。")



