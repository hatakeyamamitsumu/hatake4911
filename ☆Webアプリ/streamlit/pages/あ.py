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
st.title('物体セグメンテーションアプリ')
st.write('jpgファイルの方が比較的うまくいきます。')

# 画像のアップロード
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # 画像を読み込む
        image = Image.open(uploaded_file)
        st.image(image, caption='アップロードされた画像', use_column_width=True)
        st.write("")
        st.write("物体セグメンテーション中...")

        # 画像をnumpy配列に変換
        image_np = np.array(image)

        # 画像をモデルに入力する形式に変換
        (h, w) = image_np.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image_np, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        # 一時ディレクトリを作成
        with tempfile.TemporaryDirectory() as temp_dir:
            segmented_images = []
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.2:
                    idx = int(detections[0, 0, i, 1])
                    class_name = CLASSES[idx]

                    # 特定のクラス（例: 人）に対するマスクを作成
                    if class_name == 'person':  # 例として'person'のクラスを選択
                        mask = detections[0, 0, i, 5:9]
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")
                        mask = mask.astype(np.uint8)
                        mask = cv2.resize(mask, (endX - startX + 1, endY - startY + 1))
                        _, mask = cv2.threshold(mask, 0.5, 255, cv2.THRESH_BINARY)
                        mask = cv2.resize(mask, (image_np.shape[1], image_np.shape[0]))

                        # マスクを元画像に適用して物体のセグメンテーションを作成
                        segmented_object = cv2.bitwise_and(image_np, image_np, mask=mask)
                        segmented_images.append((segmented_object, class_name))

                        # セグメンテーション結果の画像を保存
                        image_path = os.path.join(temp_dir, f"segmented_object_{i}.png")
                        cv2.imwrite(image_path, cv2.cvtColor(segmented_object, cv2.COLOR_RGB2BGR))

            if segmented_images:
                # セグメンテーションされた画像を表示
                cols = st.columns(4)
                for i, (segmented_object, class_name) in enumerate(segmented_images):
                    pil_image = Image.fromarray(segmented_object)
                    col = cols[i % 4]
                    col.image(pil_image, caption=f"{class_name}", use_column_width=True)

                # ZIPファイルを作成
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for i, (_, class_name) in enumerate(segmented_images):
                        image_path = os.path.join(temp_dir, f"segmented_object_{i}.png")
                        zip_file.write(image_path, f"segmented_object_{i}.png")

                # ZIPファイルをダウンロードボタンとして提供
                st.download_button(
                    label="Download All Segmented Objects",
                    data=zip_buffer.getvalue(),
                    file_name="segmented_objects.zip",
                    mime="application/zip"
                )
            else:
                st.write("セグメンテーションできませんでした。")

    except Exception as e:
        st.write("セグメンテーションできませんでした。")
        st.error(f"エラーが発生しました: {e}")
