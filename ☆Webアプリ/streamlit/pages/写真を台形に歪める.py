import streamlit as st
import cv2
import numpy as np

def perspective_transform(img, src_pts, dst_pts):
    # 画像のサイズを取得
    height, width, _ = img.shape

    # 台形変換の行列を計算
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # 台形変換を適用
    result = cv2.warpPerspective(img, matrix, (width, height))

    return result

def main():
    st.title("Perspective Transform App")

    # 画像ファイルのアップロード
    uploaded_file = st.file_uploader("画像ファイルをアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # アップロードされた画像を読み込み
        img = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # デフォルトの座標を設定
        default_src_pts = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)
        default_dst_pts = np.array([[width * 0.25, width*0.2],
                                    [width * 0.75, width*0.1],
                                    [width, height*0.5],
                                    [0, height*0.8]], dtype=np.float32)

        # スライダーで調節する座標を取得
        src_pts = st.slider("変換前の4点の座標", 0.0, width, default_src_pts)
        dst_pts = st.slider("変換後の4点の座標", 0.0, width, default_dst_pts)

        # 画像を変換
        transformed_image = perspective_transform(img, src_pts, dst_pts)

        # オリジナルと変換後の画像を表示
        st.image(cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB), caption='Perspective Transformed Image', use_column_width=True)

        # 変換後の画像をファイルとして保存
        st.markdown("### Download Transformed Image")
        st.download_button(label="Download", data=cv2.imencode('.jpg', transformed_image)[1].tobytes(), file_name='Perspective_Transformed.jpg', mime='image/jpg')

if __name__ == "__main__":
    main()

