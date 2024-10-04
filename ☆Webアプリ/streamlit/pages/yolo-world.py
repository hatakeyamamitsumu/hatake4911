import streamlit as st
from ultralytics import YOLOWorld
from PIL import Image, ImageDraw

# 　YOLO-Worldモデルの読み込み
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s.pt')

# 動画ファイルのアップロード
uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'mov'])

# 動画ファイルが選択された場合
if uploaded_file is not None:
    # PILで動画を読み込む
    # (この部分、PILで直接動画を読み込む方法は限られているため、
    # OpenCVで読み込んでからPILに変換するか、別のライブラリを検討する必要があります)
    # 例：OpenCVで読み込んでからPILに変換
    import cv2
    cap = cv2.VideoCapture(uploaded_file)
    ret, frame = cap.read()
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # 物体検出の実行
    results = model.predict(source=img_pil)

    # 結果の描画 (PILで描画)
    draw = ImageDraw.Draw(img_pil)
    for *xyxy, conf, cls in results.xyxy[0]:
        x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
        draw.rectangle([(x1, y1), (x2, y2)], outline='red')

    # Streamlitで画像を表示
    st.image(img_pil)

# 静止画のアップロード
uploaded_image = st.file_uploader("Choose an image file", type=['jpg', 'png'])
if uploaded_image is not None:
    # PILで画像を読み込む
    img_pil = Image.open(uploaded_image)

    # 物体検出の実行
    results = model.predict(source=img_pil)

    # 結果の描画 (PILで描画)
    draw = ImageDraw.Draw(img_pil)
    # ... (上記と同様の描画処理)

    # Streamlitで画像を表示
    st.image(img_pil)
