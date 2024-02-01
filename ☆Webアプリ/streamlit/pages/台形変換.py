import streamlit as st
import cv2
import matplotlib.pyplot as plt
import numpy as np

def perspective_transform(img, src_pts, dst_pts):
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    result = cv2.warpPerspective(img, matrix, (img.shape[1], img.shape[0]))
    return result

def main():
    st.title("Perspective Transformation App")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # 画像の読み込み
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)

        # ユーザーが操作するための4点の座標を設定する
        src_pts = st.multiselect("Select source points", [(0, 0), (image.shape[1], 0), (image.shape[1], image.shape[0]), (0, image.shape[0])])

        if len(src_pts) != 4:
            st.warning("Please select exactly 4 source points.")
            return

        src_pts = np.array(src_pts, dtype=np.float32)

        # ユーザーが操作するための変換後の4点の座標を設定する
        dst_pts = st.multiselect("Select destination points", [(0, 0), (image.shape[1], 0), (image.shape[1], image.shape[0]), (0, image.shape[0])])

        if len(dst_pts) != 4:
            st.warning("Please select exactly 4 destination points.")
            return

        dst_pts = np.array(dst_pts, dtype=np.float32)

        # 台形変換を適用
        result = perspective_transform(image, src_pts, dst_pts)

        # オリジナルと変換後の画像を表示
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption='Original Image', use_column_width=True)
        st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB), caption='Perspective Transformed Image', use_column_width=True)

        # 変換後の画像をファイルとして保存
        st.download_button(label="Download Transformed Image", data=cv2.imencode('.jpg', cv2.cvtColor(result, cv2.COLOR_BGR2RGB))[1].tobytes(), file_name='Perspective_Transformed_Image.jpg', mime='image/jpg')

if __name__ == '__main__':
    main()
