import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

def main():
    st.title("標識作成アプリ")

    # 画像フォルダのパス
    image_folder = "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像"

    # 画像ファイルの選択
    uploaded_images = []
    st.write("### 画像を選択してください")
    for root, _, files in os.walk(image_folder):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                uploaded_images.append(os.path.join(root, file))

    selected_image_paths = st.multiselect("画像を選択してください", uploaded_images)

    ImgObjs = []
    for img_path in selected_image_paths:
        ImgObj = Image.open(img_path)
        ImgObj = ImgObj.convert('RGBA') if ImgObj.mode == "RGB" else ImgObj  # JPEGをRGBAに変換
        ImgObjs.append(ImgObj)

    WHs = [img.size for img in ImgObjs]

    wmCanvas = Image.new('RGBA', max(WHs), (255, 255, 255, 0))  # 透かし画像の生成
    for i, img in enumerate(ImgObjs):
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

    if st.button("画像をダウンロード"):
        data = download_image(WMedImage)
        st.download_button(
            label="ここをクリックしてダウンロード",
            data=data,
            file_name='合成された画像.png',
            mime='image/png'
        )

if __name__ == '__main__':
    main()
