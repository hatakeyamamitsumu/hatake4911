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
    face_positions = []
    face_images = []
    for face in faces:
        x, y, width, height = face['box']
        face_positions.append((x, y, width, height))
        # 顔を切り取り
        face_image = image[y:y+height, x:x+width]
        face_images.append(face_image)
    return face_positions, face_images

def apply_mosaic(image, face_positions, scale=0.2):
    for (x, y, width, height) in face_positions:
        # 顔の部分を切り取る
        face = image[y:y+height, x:x+width]
        # 顔の部分にモザイク処理を適用
        face = cv2.resize(face, (0, 0), fx=scale, fy=scale)
        face = cv2.resize(face, (width, height), interpolation=cv2.INTER_NEAREST)
        # モザイクをかけた顔を元の画像に戻す
        image[y:y+height, x:x+width] = face
    return image

st.title("写真の顔を加工")
st.write("JPG画像をアップロードしてください。")

# 画像のアップロード
uploaded_file = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされた画像を読み込む
    image = Image.open(uploaded_file).convert("RGB")
    # OpenCV形式に変換
    image_cv = np.array(image)
    # 顔認識を実行
    face_positions, face_images = detect_faces(image_cv.copy())

    # 検出された顔をチェックボックスで選択
    selected_faces = []
    for i, (x, y, width, height) in enumerate(face_positions):
        if st.checkbox(f"顔 {i+1} (x={x}, y={y}, w={width}, h={height})"):
            selected_faces.append((x, y, width, height))

    # モザイク処理オプション
    if st.button("モザイク処理を適用しますか？"):
        if selected_faces:
            # 選択された顔にモザイク処理を適用
            result_image_mosaic = apply_mosaic(image_cv.copy(), selected_faces)
            # モザイクをかけた結果の画像を表示
            st.image(result_image_mosaic, caption="モザイク処理後の画像", use_column_width=True)
            
            # モザイクをかけた画像をダウンロード
            result_image_pil = Image.fromarray(result_image_mosaic)
            mosaic_buffer = io.BytesIO()
            result_image_pil.save(mosaic_buffer, format='JPEG')
            mosaic_buffer.seek(0)
            st.download_button(
                label='モザイクをかけた写真をダウンロード',
                data=mosaic_buffer,
                file_name='mosaic_image.jpg',
                mime='image/jpeg'
            )
        else:
            st.write("モザイク処理を適用する顔を選択してください。")

    # 顔画像のダウンロードオプション
    if st.button("モザイクをかけずに、顔を切り取ってダウンロードしますか？"):
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
            label='ZIPファイルに顔をまとめてダウンロード',
            data=zip_buffer,
            file_name='extracted_faces.zip',
            mime='application/zip'
        )

    # 顔の位置を描画した画像を表示
    for (x, y, width, height) in face_positions:
        cv2.rectangle(image_cv, (x, y), (x + width, y + height), (255, 0, 0), 1)
    st.image(image_cv, caption="認識結果", use_column_width=True)
