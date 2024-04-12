import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

def main():
    st.title("標識（？）作成アプリ")
    st.write("当初は標識を作成するアプリを作る予定でしたが、大幅に脱線しました・・・・。")
    st.write("それぞれのリストからお好みの絵を選択して重ねてください。")
    st.write("写真をアップロードする場合は、一番上のリストは「なし」を選択してください。")
    
    # 一番目のアップローダーからの画像を表示
    uploaded_image_first = st.file_uploader("一番目のアップローダーから画像をアップロードしてください", type=["jpg", "jpeg", "png"])
    if uploaded_image_first is not None:
        uploaded_image_first = Image.open(uploaded_image_first)
        st.image(uploaded_image_first, caption='一番目のアップローダーからの画像')

    # 画像フォルダのパス
    image_folders = [
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第一層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第二層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第三層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第四層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第五層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第六層",
    ]

    # 画像アップローダー
    uploaded_image_top = st.file_uploader("上に重ねる写真をアップロードしてください", type=["jpg", "jpeg", "png"])
    uploaded_image_bottom = st.file_uploader("下に重ねる写真をアップロードしてください", type=["jpg", "jpeg", "png"])

    # 画像リストの初期化
    uploaded_images = []

    # 第一層の画像を追加
    if uploaded_image_first is not None:
        uploaded_images.append(center_align(uploaded_image_first))

    # 画像ファイルの選択（第一〜三層）
    for folder in image_folders[:3]:
        image_files = os.listdir(folder)
        selected_image = st.selectbox("", image_files, index=0)
        uploaded_images.append(center_align(Image.open(os.path.join(folder, selected_image))))

    # 画像ファイルの選択（第四〜六層）
    for folder in image_folders[3:]:
        image_files = os.listdir(folder)
        selected_image = st.selectbox("", image_files, index=0)
        uploaded_images.append(center_align(Image.open(os.path.join(folder, selected_image))))

    # 上に重ねる画像がアップロードされた場合
    if uploaded_image_top is not None:
        uploaded_image_top = Image.open(uploaded_image_top)
        uploaded_images.append(center_align(uploaded_image_top))

    # 下に重ねる画像がアップロードされた場合
    if uploaded_image_bottom is not None:
        uploaded_image_bottom = Image.open(uploaded_image_bottom)
        uploaded_images.append(center_align(uploaded_image_bottom))

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

def center_align(img):
    width, height = img.size
    new_img = Image.new("RGBA", (max(width, height), max(width, height)), (255, 255, 255, 0))
    position = ((max(width, height) - width) // 2, (max(width, height) - height) // 2)
    new_img.paste(img, position)
    return new_img

if __name__ == '__main__':
    main()
