import streamlit as st
import qrcode
from PIL import Image
import io
import base64

# ユーザーにデータを入力させる
data = st.text_input("QRコードにしたい文字列を入力してください:")

# データが入力されていればQRコードを作成
if data:
    # QRコードを作成
    qr_img = qrcode.make(data)
    
    # 画像をバイナリデータとして取得
    img_byte_array = io.BytesIO()
    qr_img.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()

    # Streamlitで画像を表示
    st.image(qr_img)

    # 一時的にファイルとして保存
    temp_file = st.file_uploader("QRコードをダウンロードするための一時ファイル", type=["png"], key="temp_file")

    if temp_file is not None:
        temp_file.write(img_byte_array)

    # ダウンロードボタンを表示
    if st.button("QRコードをダウンロード"):
        st.download_button(
            label="QRコード.pngをダウンロード",
            data=temp_file.getvalue(),
            key="download_qr_button",
            file_name="QRコード.png",
        )
else:
    st.warning("データが入力されていません。QRコードにしたい文字列を入力してください。")


