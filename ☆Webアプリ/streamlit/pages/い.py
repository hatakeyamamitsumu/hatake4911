import streamlit as st
import numpy as np
from PIL import Image
import cv2
import torch
from torchvision import models, transforms
import io

# Mask R-CNNモデルの読み込み
model = models.detection.maskrcnn_resnet50_fpn(pretrained=True)
model.eval()

# 前処理用の変換
preprocess = transforms.Compose([
    transforms.ToTensor()
])

def get_prediction(img, threshold=0.5):
    # 画像の前処理
    img_tensor = preprocess(img).unsqueeze(0)
    with torch.no_grad():
        predictions = model(img_tensor)
    
    # スコアがしきい値を超える予測を選択
    pred_score = predictions[0]['scores'].detach().numpy()
    pred_boxes = predictions[0]['boxes'].detach().numpy()
    pred_masks = predictions[0]['masks'].detach().numpy()
    
    pred_boxes = pred_boxes[pred_score >= threshold].astype(np.int32)
    pred_masks = pred_masks[pred_score >= threshold]
    pred_masks = pred_masks > threshold
    
    return pred_boxes, pred_masks

def draw_segmentation_map(image, boxes, masks):
    alpha = 0.5  # マスクの透明度
    for i in range(len(masks)):
        color = np.random.randint(0, 255, 3).tolist()
        for j in range(masks[i].shape[1]):
            for k in range(masks[i].shape[2]):
                if masks[i, 0, j, k]:
                    image[j, k, :] = alpha * image[j, k, :] + (1 - alpha) * np.array(color)
    
    # 境界ボックスを描画
    for box in boxes:
        cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
    
    return image

st.title("インスタンスセグメンテーションアプリ")
st.write("jpg画像をアップロードしてください。")

# 画像のアップロード
uploaded_file = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされた画像を読み込む
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    
    # インスタンスセグメンテーションを実行
    boxes, masks = get_prediction(image_np)
    
    # セグメンテーション結果を描画
    segmented_image = draw_segmentation_map(image_np.copy(), boxes, masks)
    
    # 結果の画像を表示
    st.image(segmented_image, caption="インスタンスセグメンテーション結果", use_column_width=True)
    
    # PNG形式でダウンロードボタンを追加
    def download_image(image, filename='segmented_image.png'):
        img_pil = Image.fromarray(image)
        img_io = io.BytesIO()
        img_pil.save(img_io, format='PNG')
        img_io.seek(0)
        st.download_button(label='ダウンロード', data=img_io, file_name=filename, mime='image/png')
    
    download_image(segmented_image)
