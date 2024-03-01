import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def download_font(font_url, font_path):
    response = requests.get(font_url)
    with open(font_path, 'wb') as f:
        f.write(response.content)

def text_to_image(text, font_size=20):
    # 画像サイズと背景色
    width, height = 300, 100
    background_color = (255, 255, 255)  # 白色

    # フォントの設定
    font_url = "https://fonts.gstatic.com/s/roboto/v27/KFOmCnqEu92Fr1Mu4mxM.woff2"
    font_path = "roboto.woff2"
    download_font(font_url, font_path)
    font = ImageFont.truetype(font_path, font_size)

    # 画像の作成と描画
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # テキストの描画位置
    text_width, text_height = draw.textsize(text, font)
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # テキストの描画
    draw.text((x, y), text, fill=(0, 0, 0), font=font)

    return image

def main():
    st.title('Text to Image Converter')

    # テキスト入力
    input_text = st.text_input('Enter Text:', 'Hello, Streamlit!')

    # フォントサイズのスライダー
    font_size = st.slider('Font Size', min_value=10, max_value=50, value=20)

    # 画像生成
    generated_image = text_to_image(input_text, font_size)

    # 生成した画像を表示
    st.image(generated_image, caption='Generated Image', use_column_width=True)

if __name__ == "__main__":
    main()
