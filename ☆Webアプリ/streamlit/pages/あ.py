import streamlit as st
import numpy as np
from PIL import Image
import cv2
from mtcnn import MTCNN
import zipfile
import io

# MTCNNの顔検出器を読み込む
detector = MTCNN()

def detect_faces(image):
    # 顔を検出
    faces = detector.detect_faces(image)
    face_images = []
    for face in faces:
        x, y, width, height = face['box']
        cv2.rectangle(image, (x, y), (x + width, y + height), (255, 0, 0), 2)
        # 顔を切り取り
        face_image = image[y:y+height, x:x+width]
        face_images.append(face_image)
    return image, face_images

st.title("顔認識アプリ")
st.write("jpg画像をアップロードしてください。")

# 画像のアップロード
uploaded_file = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされた画像を読み込む
    image = Image.open(uploaded_file).convert("RGB")
    # OpenCV形式に変換
    image = np.array(image)
    # 顔認識を実行
    result_image, face_images = detect_faces(image)
    # 結果の画像を表示
    st.image(result_image, caption="認識結果", use_column_width=True)
    
    # 顔画像をzipファイルに追加
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for i, face_image in enumerate(face_images):
            # PIL Imageに変換してzipファイルに追加
            face_pil = Image.fromarray(face_image)
            face_bytes = io.BytesIO()
            face_pil.save(face_bytes, format='JPEG')
            zip_file.writestr(f'face_{i+1}.jpg', face_bytes.getvalue())
    
    # zipファイルをダウンロードするリンクを表示
    zip_buffer.seek(0)
    st.download_button(
        label='Download Extracted Faces as ZIP',
        data=zip_buffer,
        file_name='extracted_faces.zip',
        mime='application/zip'
    )
