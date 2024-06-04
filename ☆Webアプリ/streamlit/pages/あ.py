import streamlit as st
from PIL import Image
import pytesseract
import pyocr.builders

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

# 画像アップロードエリア
selected_image = st.file_uploader('画像をアップロード', type=['jpg', 'jpeg', 'png'])

# 処理を実行
if selected_image:
    # オリジナル画像を表示
    original_image = st.empty()
    original_image.image(selected_image)

    # 結果画像を表示
    result_image = st.empty()

    # TesseractとOCRエンジンを初期化
    reader = pytesseract.image_to_string(selected_image, config='--psm 10')
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)

    # 画像を読み込み、NumPy配列に変換
    pil_image = Image.open(selected_image)
    image_array = np.array(pil_image)

    # OCR処理を実行
    result = reader.readtext(image_array, builder=builder)

    # 認識結果を描画
    draw = ImageDraw.Draw(pil_image)
    for box, text in result.items():
        # 認識領域に矩形を描画
        draw.rectangle(box, outline=(0, 0, 255), width=3)

        # 認識結果のテキストを表示
        st.write(text)

    # 結果画像を表示
    result_image.image(pil_image)
