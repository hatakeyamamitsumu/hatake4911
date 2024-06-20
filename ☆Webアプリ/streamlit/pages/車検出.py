import streamlit as st
import numpy as np
import cv2

# YOLOv3の設定
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Streamlitアプリケーションの設定
st.title("車の検出アプリ")
st.write("画像をアップロードしてください。")

# 画像のアップロード
uploaded_file = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされた画像を読み込む
    image = np.array(Image.open(uploaded_file))

    # YOLOv3で車の検出を行う関数
    def detect_cars_yolo(image):
        height, width, channels = image.shape

        # 画像をネットワークに入力する形式に変換
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []

        # 検出された物体の情報を取得
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and class_id == 2:  # class_idが2は車を表す
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # 物体の矩形の座標を計算
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # 非最大抑制を適用して重複する物体を除去
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        # 検出された車に矩形を描画
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return image

    # 検出実行
    result_image = detect_cars_yolo(image)

    # 結果の画像を表示
    st.image(result_image, caption="車の検出結果", use_column_width=True)
