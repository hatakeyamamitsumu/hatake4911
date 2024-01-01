import streamlit as st
import numpy as np
from PIL import Image

# Streamlit アプリのタイトル
st.title("RGB調整アプリ")

# 画像のアップロード
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされた画像を表示
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像", use_column_width=True)

    # 画像のRGBデータを取得
    img_array = np.array(image)

    # RGB値のスライダーを作成
    r_value = st.slider("R値", 0, 255, 128)
    g_value = st.slider("G値", 0, 255, 128)
    b_value = st.slider("B値", 0, 255, 128)

    # RGB値を変更して新しい画像を作成
    modified_image_array = np.stack([img_array[:, :, 0] * (r_value / 255),
                                     img_array[:, :, 1] * (g_value / 255),
                                     img_array[:, :, 2] * (b_value / 255)], axis=-1)

    modified_image = Image.fromarray((modified_image_array).astype(np.uint8))

    # 調整された画像を表示
    st.image(modified_image, caption="RGB調整後の画像", use_column_width=True)

