import streamlit as st
from ultralytics import YOLOWorld
from PIL import Image, ImageDraw
import cv2

def detect_objects(img_path, model, conf_thres=0.5, iou_thres=0.45):
    # 画像を読み込む
    img = Image.open(img_path)

    # YOLOv8で物体検出
    results = model.predict(source=img, conf=conf_thres, iou=iou_thres)

    # 結果を描画
    draw = ImageDraw.Draw(img)
    for *xyxy, conf, cls in results.xyxy[0]:
        x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
        draw.rectangle([(x1, y1), (x2, y2)], outline='red')

    return img

# YOLO-Worldモデルの読み込み
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s.pt')

# 画像ファイルのアップロード
uploaded_image = st.file_uploader("Choose an image file", type=['jpg', 'png'])
if uploaded_image is not None:
    # 画像の保存
    with open('temp.jpg', 'wb') as f:
        f.write(uploaded_image.getbuffer())

    # 物体検出
    result_img = detect_objects('temp.jpg', model)

    # 結果を表示
    st.image(result_img)

# 動画ファイルのアップロード
uploaded_video = st.file_uploader("Choose a video file", type=['mp4', 'mov'])
if uploaded_video is not None:
    # OpenCVで動画を読み込む
    cap = cv2.VideoCapture(uploaded_video)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # OpenCVの画像をPILに変換
        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # 物体検出
        result_img = detect_objects(img_pil, model)

        # Streamlitで画像を表示
        st.image(result_img)

    cap.release()
