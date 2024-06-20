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

    # 検出結果のプロットとNMSの適用
    (h, w) = image_np.shape[:2]
    bboxes = []
    confidences = []
    class_ids = []

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > confidence_threshold:
            class_id = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            bboxes.append([startX, startY, endX, endY])
            confidences.append(float(confidence))
            class_ids.append(class_id)

    # Non-Maximum Suppressionを適用
    indices = cv2.dnn.NMSBoxes(bboxes, confidences, confidence_threshold, nms_threshold)

    # NMSで選択されたインデックスに基づいて検出結果を描画
    colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    for i in indices:
        i = i[0]
        box = bboxes[i]
        startX, startY, endX, endY = box[0], box[1], box[2], box[3]
        class_id = class_ids[i]
        label = f"{CLASSES[class_id]}: {confidences[i]:.2f}"
        color = colors[class_id]
        cv2.rectangle(image_np, (startX, startY), (endX, endY), color, 2)
        cv2.putText(image_np, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # 検出結果の画像を表示
    detected_image = Image.fromarray(image_np)
    st.image(detected_image, caption='検出結果', use_column_width=True)

    # 検出されたオブジェクトのラベルと信頼度を表示
    st.write("検出されたオブジェクト:")
    for i in indices:
        i = i[0]
        class_id = class_ids[i]
        label = f"{CLASSES[class_id]} (信頼度: {confidences[i]:.2f})"
        st.write(label)
