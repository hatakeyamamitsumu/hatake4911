import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import zipfile
import tempfile
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


# モデルの読み込み
MODEL_PATH = '/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/mobilenet_iter_73000.caffemodel'
PROTOTXT_PATH = '/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/deploy.prototxt'
net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)

# Streamlitアプリケーションの設定
st.title('物体検出アプリ')
st.write('jpgファイルの方が比較的うまくいきます。')
# 画像のアップロード
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
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

        # 一時ディレクトリを作成
        with tempfile.TemporaryDirectory() as temp_dir:
            detected_images = []
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.2:
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    label = f"{CLASSES[idx]}: {confidence:.2f}"

                    # 画像から検出された部分を切り取る
                    detected_object = image_np[startY:endY, startX:endX]

                    # 幅または高さがゼロでないことを確認
                    if detected_object.shape[0] > 0 and detected_object.shape[1] > 0:
                        # 切り取った部分をPIL画像に変換
                        pil_image = Image.fromarray(detected_object)
                        detected_images.append((pil_image, label))

                        # 検出結果の画像を保存
                        image_path = os.path.join(temp_dir, f"detected_object_{i}.png")
                        pil_image.save(image_path)

            if detected_images:
                # 検出された画像を小さく表示
                cols = st.columns(4)
                for i, (pil_image, label) in enumerate(detected_images):
                    col = cols[i % 4]
                    col.image(pil_image, caption=f"{label}", use_column_width=True)

                # ZIPファイルを作成
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for i, (pil_image, label) in enumerate(detected_images):
                        image_path = os.path.join(temp_dir, f"detected_object_{i}.png")
                        zip_file.write(image_path, f"detected_object_{i}.png")

                # ZIPファイルをダウンロードボタンとして提供
                st.download_button(
                    label="Download All Detected Objects",
                    data=zip_buffer.getvalue(),
                    file_name="detected_objects.zip",
                    mime="application/zip"
                )
            else:
                st.write("検出できませんでした。")

    except Exception as e:
        st.write("検出できませんでした。")
        st.error(f"エラーが発生しました: {e}")
