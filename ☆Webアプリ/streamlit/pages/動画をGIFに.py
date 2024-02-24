import streamlit as st
from moviepy.editor import VideoFileClip
import base64

def convert_to_gif(input_video, output_gif, fps=10, resize_percentage=None):
    clip = VideoFileClip(input_video)

    # 動画サイズ変更
    if resize_percentage:
        resize_factor = resize_percentage / 100.0
        clip = clip.resize(resize_factor)

    clip.write_gif(output_gif, fps=fps)

def main():
    st.title("動画をGIFに変換するアプリ")

    # 動画ファイルのアップロード
    uploaded_file = st.file_uploader("動画ファイルをアップロードしてください", type=["mp4", "avi", "mov"])

    if uploaded_file is not None:
        # 出力GIFファイル名の入力
        output_gif_name = st.text_input("出力GIFファイル名を入力してください", "output_animation.gif")

        # FPSの入力
        fps = st.slider("変換するGIFのフレームレートを選択してください", min_value=1, max_value=30, value=10)

        # サイズ変更のスライダー
        resize_percentage = st.slider("動画のサイズを変更する（元の大きさの何％か）", min_value=1, max_value=100, value=100)

        # 変換ボタン
        if st.button("動画をGIFに変換"):
            # 変換処理
            convert_to_gif(uploaded_file, output_gif_name, fps, resize_percentage)
            st.success("変換が完了しました！")

            # 変換後のGIFを表示
            st.image(output_gif_name, use_column_width=True)

            # ダウンロードボタン
            download_button_str = f"ダウンロード {output_gif_name}"
            download_button_id = f"download_button_{output_gif_name}"
            st.download_button(label=download_button_str, key=download_button_id, data=uploaded_file, file_name=output_gif_name)

if __name__ == "__main__":
    main()
