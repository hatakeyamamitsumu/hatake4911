import streamlit as st
from moviepy.editor import VideoFileClip

def convert_video_to_gif(input_file, output_file, fps=10, resize_percentage=None):
    if input_file.name.endswith(('.mp4', '.avi', '.mov')):
        clip = VideoFileClip(input_file)

        # 動画サイズ変更
        if resize_percentage:
            resize_factor = resize_percentage / 100.0
            clip = clip.resize(resize_factor)

        clip.write_gif(output_file, fps=fps)
    else:
        st.error("サポートされていない動画ファイル形式です。対応する形式をアップロードしてください。")

def main():
    st.title("動画をGIFに変換するアプリ")

    # 動画ファイルのアップロード
    uploaded_file = st.file_uploader("動画ファイルをアップロードしてください", type=["mp4", "avi", "mov", "gif"])

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
            convert_video_to_gif(uploaded_file, output_gif_name, fps, resize_percentage)
            st.success("変換が完了しました！")

            # 変換後のGIFを表示
            st.image(output_gif_name, use_column_width=True)

if __name__ == "__main__":
    main()
