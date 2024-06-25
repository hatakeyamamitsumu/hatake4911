import streamlit as st
import numpy as np
from PIL import Image
import cv2
from mtcnn import MTCNN
from io import BytesIO
import base64

# MTCNNの顔検出器を読み込む
detector = MTCNN()

def detect_faces(image):
    # 顔を検出
    faces = detector.detect_faces(image)
    # 顔の位置を取得
    face_positions = [(face['box'][0], face['box'][1], face['box'][2], face['box'][3]) for face in faces]
    return face_positions

def apply_mosaic(image, face_positions, scale=0.05):
    for (x, y, width, height) in face_positions:
        # 顔の部分を切り取る
        face = image[y:y+height, x:x+width]
        # 顔の部分にモザイク処理を適用
        face = cv2.resize(face, (0, 0), fx=scale, fy=scale)
        face = cv2.resize(face, (width, height), interpolation=cv2.INTER_NEAREST)
        # モザイクをかけた顔を元の画像に戻す
        image[y:y+height, x:x+width] = face
    return image

def draw_transparent_rectangle(image, face_positions, alpha=0.5):
    overlay = image.copy()
    for (x, y, width, height) in face_positions:
        cv2.rectangle(overlay, (x, y), (x + width, y + height), (255, 0, 0), -1)
    # 画像を重ね合わせる
    return cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/jpg;base64,{img_str}" download="{filename}">{text}</a>'
    return href

st.title("顔認識アプリ")
st.write("jpg画像をアップロードしてください。")

# 画像のアップロード
uploaded_file = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされた画像を読み込む
    image = Image.open(uploaded_file)
    # OpenCV形式に変換
    image = np.array(image)
    # 顔認識を実行
    face_positions = detect_faces(image)
    # モザイク処理を適用
    result_image = apply_mosaic(image, face_positions)
    # 半透明の矩形を描画
    result_image_with_rect = draw_transparent_rectangle(result_image, face_positions)
    # OpenCVのBGR色空間からPILのRGB色空間に変換
    result_image_rgb = cv2.cvtColor(result_image_with_rect, cv2.COLOR_BGR2RGB)
    # 結果の画像を表示
    st.image(result_image_rgb, caption="認識結果", use_column_width=True)

    # ダウンロードボタンを追加
    result_pil_image = Image.fromarray(result_image_rgb)
    st.markdown(get_image_download_link(result_pil_image, "mosaic_image.jpg", "Click here to download"), unsafe_allow_html=True)

# サイドバーに情報を表示
st.sidebar.title("About")
st.sidebar.info(
    "これはStreamlitを使用してアップロードされた画像にモザイク処理を施すシンプルなアプリです。"
    "\n\n顔の検出にはMTCNNを使用し、モザイク処理にはOpenCVを使用しています。"
)
