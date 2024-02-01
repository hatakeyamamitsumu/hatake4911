import streamlit as st
import cv2
import numpy as np

# 変換前、変換後の4点の座標を設定する
src_pts = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32)

def perspective_transform(image, dst_pts):
  """
  画像を台形変換する関数

  Args:
    image: 入力画像
    dst_pts: 変換後の4点の座標

  Returns:
    変換後の画像
  """

  # 台形変換の行列を計算
  matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)

  # 台形変換を適用
  result = cv2.warpPerspective(image, matrix, (image.shape[1], image.shape[0]))

  return result

def main():
  """
  メイン関数
  """

  # 画像のアップロード
  uploaded_file = st.file_uploader("画像をアップロードしてください")

  # スライダーの設置
  top_left_x = st.slider("左上のX座標", 0.0, 1.0, 0.25, 0.01)
  top_left_y = st.slider("左上のY座標", 0.0, 1.0, 0.2, 0.01)
  top_right_x = st.slider("右上のX座標", 0.0, 1.0, 0.75, 0.01)
  top_right_y = st.slider("右上のY座標", 0.0, 1.0, 0.1, 0.01)

  # 変換後の4点の座標を設定
  dst_pts = np.array([[image.shape[1] * top_left_x, image.shape[0] * top_left_y],
                      [image.shape[1] * top_right_x, image.shape[0] * top_right_y],
                      [image.shape[1], image.shape[0]],
                      [0, image.shape[0]]], dtype=np.float32)

  # 画像がアップロードされた場合
  if uploaded_file is not None:

    # 画像を読み込み
    image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # 画像を台形変換
    result = perspective_transform(image, dst_pts)

    # オリジナルと変換後の画像を表示
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="オリジナル")
    st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB), caption="台形変換後")

if __name__ == "__main__":
  main()
