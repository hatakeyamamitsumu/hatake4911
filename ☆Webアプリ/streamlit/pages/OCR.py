from PIL import Image, ImageDraw
import easyocr
import streamlit as st
st.title("easyocrを使った簡単な写真の中の文字読み取り")
st.write("jpgファイルをアップロードしてください")
reader = easyocr.Reader(['ja','en'])
selected_image = st.file_uploader('upload image', type='jpg')

original_image = st.empty()
result_image = st.empty()

if (selected_image != None):
    original_image.image(selected_image)
    pil = Image.open(selected_image)
    result = reader.readtext(pil)
    draw = ImageDraw.Draw(pil)
    for each_result in result:
        draw.rectangle(tuple(each_result[0][0] + each_result[0][2]), outline=(0, 0, 255), width=3)
        st.write(each_result[1])
    result_image.image(pil)
