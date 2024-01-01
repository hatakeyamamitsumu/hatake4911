import streamlit as st
import numpy as np
from PIL import Image
import io

def adjust_rgb_hsv(image, r_value, g_value, b_value, hue, saturation, value):
    # RGBをHSVに変換
    image_hsv = image.convert("HSV")
    image_hsv_array = np.array(image_hsv)

    # 色相、彩度、明度の調整
    image_hsv_array[:, :, 0] = (image_hsv_array[:, :, 0] + hue) % 256
    image_hsv_array[:, :, 1] = np.clip(image_hsv_array[:, :, 1] * saturation, 0, 255)
    image_hsv_array[:, :, 2] = np.clip(image_hsv_array[:, :, 2] * value, 0, 255)

    # HSVをRGBに戻し、RGB値の調整
    modified_image_array = np.stack([image_hsv_array[:, :, 0] * (r_value / 255),
                                     image_hsv_array[:, :, 1] * (g_value / 255),
                                     image_hsv_array[:, :, 2] * (b_value / 255)], axis=-1)

    # HSVから戻ったRGBを0から255の範囲にクリッピング
    modified_image_array = np.clip(modified_image_array, 0, 255)

    # 画像をuint8型に変換してPIL Imageにする
    modified_image = Image.fromarray(modified_image_array.astype(np.uint8), 'RGB')
    return modified_image

# Streamlit アプリのタイトル
st.title("RGB・HSV調整アプリ")

# 画像のアップロード
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされた画像を表示
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像", use_column_width=True)

    # RGB値のスライダーを作成
    r_value = st.slider("R値", 0, 255, 128)
    g_value = st.slider("G値", 0, 255, 128)
    b_value = st.slider("B値", 0, 255, 128)

    # 色相、彩度、明度のスライダーを作成
    hue_value = st.slider("色相", -180, 180, 0)
    saturation_value = st.slider("彩度", 0.0, 2.0, 1.0)
    value_value = st.slider("明度", 0.0, 2.0, 1.0)

    # RGBとHSVの値を同時に変更して新しい画像を作成
    modified_image = adjust_rgb_hsv(image, r_value, g_value, b_value, hue_value, saturation_value, value_value)

    # 調整された画像を表示
    st.image(modified_image, caption="RGB・HSV調整後の画像", use_column_width=True)

    # 調整された画像をダウンロード
    if st.button("画像をダウンロード"):
        # Pillowで画像を作成し、バイトデータに変換
        modified_image_bytes = io.BytesIO()
        modified_image.save(modified_image_bytes, format='JPEG')

        # ダウンロードボタンに渡す
        st.download_button("ダウンロード", modified_image_bytes.getvalue(), file_name="modified_image.jpg", key="download")

