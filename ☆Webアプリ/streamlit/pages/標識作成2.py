import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

def main():
    st.title("標識（？）作成アプリ")
    st.write("当初は標識を作成するアプリを作る予定でしたが、大幅に脱線しました・・・。")
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
        ImgObj = Image.open(uploaded_image)
        ImgObj = ImgObj.convert('RGBA') if ImgObj.mode == "RGB" else ImgObj  # JPEGをRGBAに変換
        uploaded_images = [ImgObj]

    else:
        uploaded_images = []

    # 画像ファイルの選択
    for folder in image_folders:
        image_files = os.listdir(folder)
        selected_image = st.selectbox("", image_files, index=0)
        uploaded_images.append(Image.open(os.path.join(folder, selected_image)))

    ImgObjs = []
    for img in uploaded_images:
        ImgObj = img.copy()
        ImgObj.thumbnail((ImgObj.size[0], ImgObj.size[1]))  # サイズの調整
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
