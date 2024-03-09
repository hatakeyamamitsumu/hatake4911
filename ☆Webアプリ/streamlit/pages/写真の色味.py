import streamlit as st
import os
import cv2
import numpy as np

# 青色のHSV範囲
HUE_MIN = 100
HUE_MAX = 140
SATURATION_MIN = 100
VALUE_MIN = 100

def main():
    st.title("aフォルダから青味の強い写真を選んで表示")

    # aフォルダ内の画像ファイル一覧を取得
    image_filenames = os.listdir("/mount/src/hatake4911/☆Webアプリ/画像")

    # 画像ファイルリストを表示
    image_file_selectbox = st.selectbox("画像ファイルを選択", image_filenames)

    # 選択された画像を読み込み
    image_path = os.path.join("/mount/src/hatake4911/☆Webアプリ/画像", image_file_selectbox)
    try:
        image = cv2.imread(image_path)
    except Exception as e:
        st.error(f"画像の読み込みに失敗しました: {e}")
        return

    # 画像の深度を確認
    depth = image.dtype

    # 深度が期待通りでない場合は変換
    if depth not in (cv2.CV_8U, cv2.CV_16U):
        image = cv2.convertScaleAbs(image, alpha=255.0)

    # 画像をHSVに変換
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 青色の範囲でマスクを作成
    mask = cv2.inRange(hsv, (HUE_MIN, SATURATION_MIN, VALUE_MIN), (HUE_MAX, 255, 255))

    # マスクされた画像を表示
    st.image(mask, caption="青色のマスク", use_column_width=True)

    # 青色の割合を計算
    blue_ratio = np.count_nonzero(mask) / (image.shape[0] * image.shape[1])

    # 青色の割合を表示
    st.write(f"青色の割合: {blue_ratio:.2%}")

    # 元画像とマスク画像を並べて表示
    st.image([image, mask], caption=["元画像", "青色のマスク"], use_column_width=True)

if __name__ == "__main__":
    main()


