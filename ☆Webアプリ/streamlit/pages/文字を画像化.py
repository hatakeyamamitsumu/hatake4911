import streamlit as st
from PIL import Image, ImageDraw, ImageFont

def text_to_image(text, font_size, output_path):
 
  width, height = 300, 100
   

  image = Image.new('RGB', (width, height), 'white')
  draw = ImageDraw.Draw(image)
   

  font = ImageFont.truetype("arial.ttf", font_size)
   

  draw.text((10, 10), text, font=font, fill='black')
   

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
