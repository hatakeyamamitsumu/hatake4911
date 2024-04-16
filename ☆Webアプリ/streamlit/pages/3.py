import streamlit as st
from PIL import Image
import os

def main():
    st.title("写真と絵を組み合わせるアプリです。")
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
    uploaded_image = st.file_uploader("写真をアップロードしてください。※一番上のリストは「なし」を選択してください。", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        ImgObj = Image.open(uploaded_image)
        ImgObj = ImgObj.convert('RGBA') if ImgObj.mode == "RGB" else ImgObj  # JPEGをRGBAに変換
        uploaded_images = [center_align_with_max_size(ImgObj, max_size=(300, 300))]

    else:
        uploaded_images = []

    # 画像ファイルの選択
    for folder in image_folders[:3]:
        image_files = os.listdir(folder)
        selected_image = st.selectbox("", image_files, index=0)
        img = Image.open(os.path.join(folder, selected_image))
        img = keep_within_max_size(img, max_size=(300, 300))  # 最大サイズ内に収める
        uploaded_images.append(center_align_with_max_size(img, max_size=(300, 300)))

    # 一番手前の画像をアップロード
    front_image = st.file_uploader("「写真の背景を操作」を使って、背景を取り除いた画像をアップロードしてみてください。.", type=["jpg", "jpeg", "png"])

    if front_image is not None:
        front_image_obj = Image.open(front_image)
        front_image_obj = front_image_obj.convert('RGBA') if front_image_obj.mode == "RGB" else front_image_obj
        front_image_obj = keep_within_max_size(front_image_obj, max_size=(300, 300))  # 最大サイズ内に収める
        
        # 4番目と5番目の画像の間に追加
        uploaded_images.insert(4, center_align_with_max_size(front_image_obj, max_size=(300, 300)))

    # 画像ファイルの選択
    for folder in image_folders[3:]:
        image_files = os.listdir(folder)
        selected_image = st.selectbox("", image_files, index=0)
        img = Image.open(os.path.join(folder, selected_image))
        img = keep_within_max_size(img, max_size=(300, 300))  # 最大サイズ内に収める
        uploaded_images.append(center_align_with_max_size(img, max_size=(300, 300)))

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

def center_align_with_max_size(img, max_size):
    """
    画像を中央揃えにし、指定された最大サイズにリサイズする
    """
    width, height = img.size
    left = (max_size[0] - width) // 2
    top = (max_size[1] - height) // 2
    new_img = Image.new("RGBA", max_size, (255, 255, 255, 0))
    new_img.paste(img, (left, top))
    return new_img

def keep_within_max_size(img, max_size):
    """
    画像の縦横の長さが指定された最大サイズ内に収まるように縮小する
    """
    width, height = img.size
    max_width, max_height = max_size
    width_ratio = max_width / width
    height_ratio = max_height / height
    # 最小の比率を選択して、縦も横も収める
    resize_ratio = min(width_ratio, height_ratio)
    new_width = int(width * resize_ratio)
    new_height = int(height * resize_ratio)
    return img.resize((new_width, new_height), Image.ANTIALIAS)

if __name__ == '__main__':
    main()
