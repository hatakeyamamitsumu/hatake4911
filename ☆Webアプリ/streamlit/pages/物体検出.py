import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# 　COCOデータセットのクラスラベルのリスト
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

# ファイルパスの存在確認
if not os.path.exists(MODEL_PATH) or not os.path.exists(PROTOTXT_PATH):
    st.error(f"モデルファイルまたはプロトファイルが見つかりません。パスを確認してください。")
else:
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
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.2:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                label = f"{CLASSES[idx]}: {confidence:.2f}"
                
                # 赤枠で囲む
                cv2.rectangle(image_np, (startX, startY), (endX, endY), (0, 0, 255), 2)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.putText(image_np, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # 検出結果の画像を表示
        detected_image = Image.fromarray(image_np)
        st.image(detected_image, caption='検出結果', use_column_width=True)

        # 検出されたオブジェクトのラベルと信頼度を表示
        st.write("検出されたオブジェクト:")
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.2:
                idx = int(detections[0, 0, i, 1])
                st.write(f"{CLASSES[idx]} (信頼度: {confidence:.2f})")
