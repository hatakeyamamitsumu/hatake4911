import streamlit as st
import numpy as np
from PIL import Image
import torch
from torchvision import models, transforms

# Mask R-CNNモデルの読み込み
@st.cache_resource
def load_model():
    model = models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    model.eval()
    return model

model = load_model()

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
    pred_score = predictions[0]['scores'].detach().cpu().numpy()
    pred_boxes = predictions[0]['boxes'].detach().cpu().numpy()
    pred_masks = predictions[0]['masks'].detach().cpu().numpy()

    pred_boxes = pred_boxes[pred_score >= threshold].astype(np.int32)
    pred_masks = pred_masks[pred_score >= threshold]
    pred_masks = pred_masks.squeeze(1) > threshold  # マスクの次元を調整

    return pred_boxes, pred_masks

def draw_segmentation_map(image, masks, selected_masks):
    alpha = 0.6  # マスクの透明度
    for i, mask_selected in enumerate(selected_masks):
        if mask_selected:
            color = np.random.randint(0, 255, 3).tolist()
            mask = masks[i]
            image[mask] = alpha * np.array(color) + (1 - alpha) * image[mask]
    
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

    # チェックボックスで各領域を選択
    selected_masks = []
    for i, box in enumerate(boxes):
        selected = st.checkbox(f"領域 {i+1} (x={box[0]}, y={box[1]}, w={box[2] - box[0]}, h={box[3] - box[1]})", value=True)
        selected_masks.append(selected)

    if st.button("色塗りを適用"):
        # セグメンテーション結果を描画
        segmented_image = draw_segmentation_map(image_np.copy(), masks, selected_masks)
        
        # セグメンテーション結果の画像を表示
        st.image(segmented_image, caption="セグメンテーション結果", use_column_width=True)
