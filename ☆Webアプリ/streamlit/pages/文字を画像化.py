import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import base64

def text_to_image(text, output_path):
    # 画像サイズと背景色を設定
    width, height = 100, 20  # 任意のサイズ
    background_color = "white"

    # 画像を作成
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 使用するフォントとテキストの設定
    font_size = 15
    font = ImageFont.truetype("/mount/src/hatake4911/☆Webアプリ/フォントファイル/HGRPRE.TTC", font_size)  # フォントは適切なものを指定
    text_color = "black"

    # テキストを中央に配置
    text_width, text_height = draw.textsize(text, font)
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # テキストを描画
    draw.text((x, y), text, font=font, fill=text_color)

    # 画像を保存
    image.save(output_path)

# Streamlitアプリ
st.title("文字を画像化")

# ダウンロードボタンが押されたかどうかの状態変数
download_button = st.button("画像をダウンロード")

if download_button:
    # 画像を作成
    text_to_image("山", "mountain.png")

    # 画像を読み込み
    image = Image.open("mountain.png")

    # ダウンロードボタンを作成
    download_btn = st.download_button(
        label="画像をダウンロード",
        data=base64.b64encode(image.tobytes()).decode(),
        file_name="mountain.png",
        key="download_button"
    )

    # 画像を表示
    st.image(image, caption="山", use_column_width=True)
