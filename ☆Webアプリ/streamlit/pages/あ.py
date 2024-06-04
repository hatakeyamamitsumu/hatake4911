import streamlit as st
from PIL import Image
import pytesseract

# タイトルと説明を表示
st.title("Streamlitで画像からテキストを抽出")
st.write("このアプリは、アップロードされた画像からテキストを抽出します。")

# 画像をアップロード
uploaded_file = st.file_uploader("画像を選択してください")

# アップロードされた画像が存在する場合
if uploaded_file:
    # 画像を読み込む
    image = Image.open(uploaded_file)

    # テキストを抽出
    text = pytesseract.image_to_string(image)

    # 抽出結果を表示
    st.write("抽出結果:")
    st.write(text)


selected_image = st.file_uploader('upload image', type='jpg')

reader = tool.image_to_string(
    img1,
    lang='jpn+eng',
    builder=pyocr.builders.TextBuilder(tesseract_layout=6)
)



original_image = st.empty()
result_image = st.empty()

if (selected_image != None):
    original_image.image(selected_image)
    pil = Image.open(selected_image)
    result = reader.readtext(np.array(pil))
    draw = ImageDraw.Draw(pil)
    for each_result in result:
        draw.rectangle(((each_result[0][0][0], each_result[0][0][1]), (each_result[0][2][0], each_result[0][2][1])), outline=(0, 0, 255), width=3)


        st.write(each_result[1])
    result_image.image(pil)
