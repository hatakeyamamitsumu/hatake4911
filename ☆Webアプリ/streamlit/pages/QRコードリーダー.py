import streamlit as st
import cv2
from pyzbar.pyzbar import decode

def read_qr_code(image):
    decoded_objects = decode(image)
    for obj in decoded_objects:
        st.info(f"QR Code Detected: {obj.data.decode('utf-8')}")
        st.image(image, caption='Captured Image', use_column_width=True)
        return True
    return False

def main():
    st.title("QR Code Reader with Streamlit")

    # カメラ入力
    picture = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if picture is not None:
        # Convert image to NumPy array
        image = cv2.imdecode(np.frombuffer(picture.read(), np.uint8), 1)

        if image is not None:
            # バイナリ形式に変換
            image_bin = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # QRコード読み取り
            if read_qr_code(image_bin):
                return  # QRコードが見つかったら処理終了

            # QRコードが見つからない場合は通常の画像表示
            st.image(image, caption='Captured Image', use_column_width=True)

if __name__ == "__main__":
    main()
