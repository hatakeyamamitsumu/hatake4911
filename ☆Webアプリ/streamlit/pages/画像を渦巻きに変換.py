import streamlit as st
import numpy as np
from PIL import Image

# Function to swirl the image
def swirl_image(image_array, strength=10, radius=1000):
    # 画像のサイズを取得
    height, width, _ = image_array.shape

    # 中心座標を計算
    center_x = width // 2
    center_y = height // 2

    # 出力画像の配列を作成
    output_array = np.empty_like(image_array)

    # 画像を渦巻き状に加工
    for y in range(height):
        for x in range(width):
            # 現在のピクセル座標から中心座標までの距離と角度を計算
            dx = x - center_x
            dy = y - center_y
            distance = np.sqrt(dx ** 2 + dy ** 2)
            angle = np.arctan2(dy, dx)

            if distance == 0:
                new_x = x
                new_y = y
            else:
                # 渦巻きの力を計算.値が大きいほど強い渦巻きになる
                swirl_strength = strength * (radius / distance) ** 0.2

                # 渦巻き効果を適用した座標を計算
                new_x = int(center_x + np.cos(angle + swirl_strength) * distance)
                new_y = int(center_y + np.sin(angle + swirl_strength) * distance)

            # 出力画像の座標範囲内の場合、ピクセル値をコピー
            if 0 <= new_x < width and 0 <= new_y < height:
                output_array[y, x] = image_array[new_y, new_x]
            else:
                output_array[y, x] = 0  # ピクセル値が範囲外の場合は黒にする

    return output_array

# Streamlit app
st.title("写真を渦巻に変換")
st.text("ダウンロード機能がありません。お手数ですがスクリーンショットしてください")

# File uploader
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image
    image = Image.open(uploaded_file)
    image_array = np.array(image)

    # Swirl parameters
    strength = st.slider("渦の強さ", min_value=1, max_value=20, value=10)
    radius = st.slider("渦の半径サイズ", min_value=100, max_value=2000, value=1000)

    # Image display width slider
    display_width = st.slider("画像サイズ", min_value=100, max_value=1000, value=600)

    # Process the image
    processed_image_array = swirl_image(image_array, strength, radius)

    # Display the original and processed images with adjustable width
    st.image([image, Image.fromarray(processed_image_array)], caption=["Original Image", "Swirled Image"], width=display_width)

