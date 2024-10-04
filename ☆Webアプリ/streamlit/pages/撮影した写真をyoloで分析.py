import streamlit as st
from ultralytics import YOLOWorld
from PIL import Image, ImageDraw

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
