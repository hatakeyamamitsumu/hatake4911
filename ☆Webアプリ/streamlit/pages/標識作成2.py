import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

def main():
    st.title("標識（？）作成アプリ")
    st.write("当初は標識を作成するアプリを作る予定でしたが、大幅に脱線しました・・・・。")
    st.write("それぞれのアップローダーからお好みの絵を選択して重ねてください。")

    # 画像フォルダのパス
    image_folders = [
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第一層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第二層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第三層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第四層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第五層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第六層",
    ]

    # アップロードされた画像
    uploaded_image1 = st.file_uploader("1つ目の写真をアップロードしてください", type=["jpg", "jpeg", "png"])
    uploaded_image2 = st.file_uploader("2つ目の写真をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image1 is not None:
        ImgObj1 = Image.open(uploaded_image1)
        ImgObj1 = ImgObj1.convert('RGBA') if ImgObj1.mode == "RGB" else ImgObj1  # JPEGをRGBAに変換
        uploaded_images = [center_align(ImgObj1)]

    else:
        uploaded_images = [None]

    if uploaded_image2 is not None:
        ImgObj2 = Image.open(uploaded_image2)
        ImgObj2 = ImgObj2.convert('RGBA') if ImgObj2.mode == "RGB" else ImgObj2  # JPEGをRGBAに変換
        uploaded_images.append(center_align(ImgObj2))

    else:
        uploaded_images.append(None)

    # 画像ファイルの選択
    for folder in image_folders:
        image_files = os.listdir(folder)
        selected_image = st.selectbox("", image_files, index=0)
        uploaded_images.append(center_align(Image.open(os.path.join(folder, selected_image))))

    # 他の画像のサイズに合わせて縮小拡大
    max_width = max(img.size[0] for img in uploaded_images)
    max_height = max(img.size[1] for img in uploaded_images)
    for i, img in enumerate(uploaded_images):
        width_ratio = max_width / img.size[0]
        height_ratio = max_height / img.size[1]
        resize_ratio = min(width_ratio, height_ratio)
        new_size = (int(img.size[0] * resize_ratio), int(img.size[1] * resize_ratio))
        uploaded_images[i] = img.resize(new_size, Image.ANTIALIAS)

    ImgObjs = uploaded_images

    wmCanvas = Image.new('RGBA', (max_width, max_height), (255, 255, 255, 0))  # 透かし画像の生成
    for i, img in enumerate(ImgObjs):
        if img is not None:
            wmCanvas.paste(img, (0, 0), img)  # 透かし画像を貼り付け

    WMedImage = wmCanvas  # 画像の合成

    # 画像を表示
    st.image(WMedImage, caption='合成された画像')

    # 画像をダウンロードするボタン
    def download_image(image, filename='合成された画像.png'):
        image.save(filename, 'PNG')
        with open(filename, 'rb') as f:
            data = f.read()
        return data

    if st.button("ダウンロードしますか？"):
        data = download_image(WMedImage)
        st.download_button
