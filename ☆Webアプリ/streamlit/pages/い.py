import streamlit as st
import cv2
import numpy as np
from PIL import Image

# COCOデータセットのクラスラベルのリスト
CLASSES = ["background", "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
           "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", 
           "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase",
           "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", 
           "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", 
           "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", 
           "sofa", "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", 
           "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", 
           "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

# モデルの読み込み
MODEL_PATH = '/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/mobilenet_iter_73000.caffemodel'
PROTOTXT_PATH = '/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/deploy.prototxt'
net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)

# Streamlitアプリケーションの設定
st.title('物体検出アプリ')

# 画像のアップロード
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 画像を読み込む
    image = Image.open(uploaded_file)
    st.image(image, caption='アップロードされた画像', use_column_width=True)
    st.write("")
    st.write("物体検出中...")

    # 画像をnumpy配列に変換
    image_np = np.array(image)

    # 画像をモデルに入力する形式に変換
    (h, w) = image_np.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image_np, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    # 検出された物体の画像を4列で表示
    col1, col2, col3, col4 = st.beta_columns(4)

    count = 0
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            label = f"{CLASSES[idx]}: {confidence:.2f}"

            # 画像から検出された部分を切り取る
            detected_object = image_np[startY:endY, startX:endX]

            # 切り取った部分をPIL画像に変換してリサイズ
            pil_image = Image.fromarray(detected_object)
            resized_image = pil_image.resize((int(pil_image.width / 4), int(pil_image.height / 4)))

            # 1/4サイズで表示
            if count % 4 == 0:
                with col1:
                    st.image(resized_image, caption=f"Detected Object {count+1}: {label}", use_column_width=True)
            elif count % 4 == 1:
                with col2:
                    st.image(resized_image, caption=f"Detected Object {count+1}: {label}", use_column_width=True)
            elif count % 4 == 2:
                with col3:
                    st.image(resized_image, caption=f"Detected Object {count+1}: {label}", use_column_width=True)
            elif count % 4 == 3:
                with col4:
                    st.image(resized_image, caption=f"Detected Object {count+1}: {label}", use_column_width=True)
            count += 1

            st.write(f"{CLASSES[idx]} (信頼度: {confidence:.2f})")

