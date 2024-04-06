import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

def main():
    st.title("標識（？）作成アプリ")
    st.write("当初は標識を作成するアプリを作る予定でしたが、大幅に脱線しました・・・・。")
    st.write("それぞれのリストからお好みの絵を選択して重ねてください。")

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
    uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        uploaded_image = Image.open(uploaded_image)
        uploaded_image = uploaded_image.convert('RGBA') if uploaded_image.mode == "RGB" else uploaded_image  # JPEGをRGBAに変換
        uploaded_images = [uploaded_image]
    else:
        uploaded_images = []

    # 画像ファイルの選択
    image_files_list = []
    for folder in image_folders:
        image_files = os.listdir(folder)
        image_files_list.append([os.path.join(folder, image_file) for image_file in image_files])

    selected_images = []
    for image_files in image_files_list:
        selected_image = st.selectbox("", image_files, index=0)
        selected_images.append(Image.open(selected_image))

    # 他の画像のサイズに合わせて縦横比を変えずにリサイズ
    max_width = max(img.size[0] for img in selected_images) if selected_images else 0
    max_height = max(img.size[1] for img in selected_images) if selected_images else 0
    for i, img in enumerate(selected_images):
        width_ratio = max_width / img.size[0]
        height_ratio = max_height / img.size[1]
        resize_ratio = min(width_ratio, height_ratio)
        new_size = (int(img.size[0] * resize_ratio), int(img.size[1] * resize_ratio))
        selected_images[i] = img.resize(new_size, Image.ANTIALIAS)

    ImgObjs = selected_images + uploaded_images

    wmCanvas = Image.new('RGBA', (max_width, max_height), (255, 255, 255, 0))  # 透かし画像の生成
    for i, img in enumerate(ImgObjs):
        offset_x = (max_width - img.size[0]) // 2
        offset_y = (max_height - img.size[1]) // 2
        wmCanvas.paste(img, (offset_x, offset_y), img)  # 透かし画像を貼り付け

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
        st.download_button(
            label="ここをクリックしてダウンロード",
            data=data,
            file_name='合成された画像.png',
            mime='image/png'
        )

if __name__ == '__main__':
    main()

