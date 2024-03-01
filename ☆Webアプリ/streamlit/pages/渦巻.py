import streamlit as st
import numpy as np
from PIL import Image

# 画像を渦巻きに変換する関数
def swirl_image(image_array, strength=10, radius=1000):
    # (コードは変更なし)

# Streamlit アプリ
st.title("写真を渦巻に変換")
st.text("画像のダウンロードはできませんが、スクリーンショットで保存できます。")

# ファイルアップローダー
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 画像を読み込む
    image = Image.open(uploaded_file)
    image_array = np.array(image)

    # 渦巻きのパラメータ
    strength = st.slider("渦の強さ", min_value=1, max_value=20, value=10)
    radius = st.slider("渦の半径サイズ", min_value=100, max_value=2000, value=1000)

    # 画像の表示幅
    display_width = st.slider("画像サイズ", min_value=100, max_value=1000, value=600)

    # 渦巻き後の画像の背景色
    bg_color = st.color_picker("渦巻き後の画像の背景色", value="#ffffff")

    # 画像を渦巻きに変換
    processed_image_array = swirl_image(image_array, strength, radius)

    # 背景色を設定して画像を表示
    processed_image = Image.fromarray(processed_image_array)
    processed_image = processed_image.convert("RGBA")
    processed_image_with_bg = Image.new("RGBA", processed_image.size, bg_color)
    processed_image_with_bg.paste(processed_image, (0, 0), processed_image)

    # オリジナル画像と渦巻き後の画像を表示
    st.image([image, processed_image_with_bg], caption=["オリジナル画像", "渦巻き後の画像"], width=display_width)

    # オリジナル画像と渦巻き後の画像のダウンロードボタン
    st.download_button(
        label="オリジナル画像をダウンロード",
        data=uploaded_file.getvalue(),
        file_name="original_image.png",
    )

    # 新しいバイト変換の方法を使用して渦巻き後の画像をダウンロード
    processed_image_bytes = processed_image_with_bg.convert("RGB").tobytes()
    st.download_button(
        label="渦巻き後の画像をダウンロード",
        data=processed_image_bytes,
        file_name="swirled_image.png",
    )
