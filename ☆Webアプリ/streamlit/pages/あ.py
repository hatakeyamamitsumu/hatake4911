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

    # 画像の前処理
    blob = cv2.dnn.blobFromImage(image_np, scalefactor=1.0/127.5, size=(300, 300), mean=(127.5, 127.5, 127.5))
    net.setInput(blob)

    # 検出結果の取得
    detections = net.forward()

    # 推論パラメータの設定
    confidence_threshold = 0.2
    nms_threshold = 0.4

    # 検出結果のプロット
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > confidence_threshold:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([image_np.shape[1], image_np.shape[0], image_np.shape[1], image_np.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")
            label = f"{CLASSES[idx]}: {confidence:.2f}"
            cv2.rectangle(image_np, (startX, startY), (endX, endY), (0, 255, 0), 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image_np, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 非最大抑制
    indices = cv2.dnn.NMSBoxes(bboxes, confidences, confidence_threshold, nms_threshold)
    for i in indices:
        i = i[0]
        box = bboxes[i]
        startX, startY, endX, endY = box.astype("int")
        label = f"{CLASSES[class_ids[i]]}: {confidences[i]:.2f}"
        cv2.rectangle(image_np, (startX, startY), (endX, endY), (0, 255, 0), 2)
        y = startY - 15 if startY - 15 > 15 else startY + 15
        cv2.putText(image_np, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 検出結果の画像を表示
    detected_image = Image.fromarray(image_np)
    st.image(detected_image, caption='検出結果', use_column_width=True)

    # 検出されたオブジェクトのラベルと信頼度を表示
    st.write("検出されたオブジェクト:")
    for i in range(len(indices)):
        idx = indices[i][0]
        label = f"{CLASSES[class_ids[idx]]} (信頼度: {confidences[idx]:.2f})"
        st.write(label)
