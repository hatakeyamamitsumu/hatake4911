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
MODEL_PATH = 'mobilenet_iter_73000.caffemodel'
PROTOTXT_PATH = 'deploy.prototxt'
net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)

# Streamlitアプリケーションの設定
st.title('物体検出アプリ')
st.write('jpgファイルの方が比較的うまくいきます。')

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

    # 検出結果をプロット
    labels = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            labels.append(CLASSES[idx])

    # 検出されたオブジェクトのリストを表示し、選択させる
    selected_label = st.selectbox("ぼかさない物体を選択してください:", labels)

    # ぼかし処理
    mask = np.zeros(image_np.shape[:2], dtype="uint8")
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])
            if CLASSES[idx] == selected_label:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(mask, (startX, startY), (endX, endY), 255, -1)

    blurred_image_np = cv2.GaussianBlur(image_np, (21, 21), 0)
    inverse_mask = cv2.bitwise_not(mask)
    foreground = cv2.bitwise_and(image_np, image_np, mask=mask)
    background = cv2.bitwise_and(blurred_image_np, blurred_image_np, mask=inverse_mask)
    final_image = cv2.add(foreground, background)

    # 検出結果の画像を表示
    detected_image = Image.fromarray(final_image)
    st.image(detected_image, caption='検出結果', use_column_width=True)
