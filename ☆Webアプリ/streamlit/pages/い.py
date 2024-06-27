import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

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

# モデルの読み込みパス
MODEL_PATH = '/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/mobilenet_iter_73000.caffemodel'
PROTOTXT_PATH = '/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/deploy.prototxt'

# ファイルの存在確認
if not os.path.exists(MODEL_PATH):
    st.error(f"モデルファイルが見つかりません: {MODEL_PATH}")
if not os.path.exists(PROTOTXT_PATH):
    st.error(f"プロトタイプファイルが見つかりません: {PROTOTXT_PATH}")

try:
    net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)
except cv2.error as e:
    st.error(f"モデルの読み込みに失敗しました: {e}")
    st.stop()

# Streamlitアプリケーションの設定
st.title('物体検出アプリ')
st.write('jpgファイルの方が比較的うまくいきます。')

# ぼかし具合を選択するスライダー
blur_strength = st.slider('ぼかし具合を選択してください (カーネルサイズ)', 1, 50, 21, step=2)

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
    mask = np.zeros(image_np.shape[:2], dtype="uint8")
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(mask, (startX, startY), (endX, endY), 255, -1)

    # ユーザーが選択した部分のみを残し、それ以外をぼかす処理
    selected_region = st.selectbox("物体検出結果から選択した部分をぼかします", options=[False, True])
    if selected_region:
        mask_inverse = cv2.bitwise_not(mask)
        blurred_image_np = cv2.GaussianBlur(image_np, (blur_strength, blur_strength), 0)
        result_image_np = np.where(mask_inverse[:, :, None] == 0, image_np, blurred_image_np)
    else:
        blurred_image_np = cv2.GaussianBlur(image_np, (blur_strength, blur_strength), 0)
        result_image_np = blurred_image_np

    # 検出結果の画像を表示
    detected_image = Image.fromarray(result_image_np)
    st.image(detected_image, caption='検出結果', use_column_width=True)

    # 検出されたオブジェクトのラベルと信頼度を表示
    st.write("検出されたオブジェクト:")
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])
            st.write(f"{CLASSES[idx]} (信頼度: {confidence:.2f})")
