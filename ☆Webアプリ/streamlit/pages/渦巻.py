import streamlit as st
import numpy as np
from PIL import Image

# 画像を渦巻きに変換する関数
def swirl_image(image_array, strength=10, radius=1000, center_x=None, center_y=None):
    # 画像のサイズを取得
    height, width, _ = image_array.shape

    # 中心座標を計算
    if center_x is None:
        center_x = width // 2
    if center_y is None:
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
                # 渦巻きの力を計算. 値が大きいほど強い渦巻きになる
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

# Streamlit アプリ
st.title("写真を渦巻に変換")
st.text("ダウンロード機能がありません。お手数ですがスクリーンショットしてください")

# ファイルアップローダー
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 画像を読み込む
    image = Image.open(uploaded_file)
    image_array = np.array(image)

    # 渦巻きのパラメータ
    strength = st.slider("渦の強さ", min_value=1, max_value=20, value=10)
    radius = st.slider("渦の半径サイズ", min_value=100, max_value=2000, value=1000)

    # 中心座標の調整
    center_x = st.slider("中心のX座標", min_value=0, max_value=image_array.shape[1], value=image_array.shape[1] // 2)
    center_y = st.slider("中心のY座標", min_value=0, max_value=image_array.shape[0], value=image_array.shape[0] // 2)

    # 画像の表示幅
    display_width = st.slider("画像サイズ", min_value=100, max_value=1000, value=600)

    # 画像を渦巻きに変換
    processed_image_array = swirl_image(image_array, strength, radius, center_x, center_y)

    # オリジナル画像と渦巻き後の画像を表示
    st.image([image, Image.fromarray(processed_image_array)], caption=["オリジナル画像", "渦巻き後の画像"], width=display_width)
