import streamlit as st
import numpy as np
from PIL import Image
import cv2

# ここでセグメンテーションされた結果とマスクを用意することを想定
# 仮の例として、単純な画像とマスクを生成する
image_size = (256, 256)
image = np.ones((image_size[0], image_size[1], 3), dtype=np.uint8) * 255  # 白色画像
mask = np.zeros((image_size[0], image_size[1]), dtype=np.uint8)
mask[50:150, 50:150] = 255  # ダミーのマスク、中央部分のみ白色

# マスクされた領域の抽出
segmented_images = []
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for i, contour in enumerate(contours):
    # マスクされた領域のバウンディングボックスを取得
    x, y, w, h = cv2.boundingRect(contour)
    # マスクされた領域を切り抜いて新しい画像として追加
    segmented_image = image[y:y+h, x:x+w].copy()
    segmented_images.append(segmented_image)

# 各セグメントされた画像を表示
st.title('セグメンテーションされた領域の表示')
for i, segment_img in enumerate(segmented_images):
    st.image(segment_img, caption=f'Segment {i+1}', use_column_width=True)
