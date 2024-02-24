import streamlit as st
from PIL import Image, ImageDraw, ImageFont

def text_to_image(text, font_size, output_path):
  # 画像サイズ
  width, height = 300, 100

  # 画像を白色で初期化
  image = Image.new('RGB', (width, height), 'white')
  draw = ImageDraw.Draw(image)

  # フォントの設定
  font =  ImageFont.load_default()

  # テキストを画像に描画
  draw.text((10, 10), text, font=font, fill='black')

  # 画像を保存
  image.save(output_path)

def main():
  st.title('テキストを画像に変換')

  text = st.text_input('変換したいテキストを入力してください')
  font_size = st.slider('フォントサイズ', 10, 50, 20)

  if st.button('変換'):
    output_path = 'output_image.png'
    text_to_image(text, font_size, output_path)

    st.image(output_path)

if __name__ == '__main__':
  main()
