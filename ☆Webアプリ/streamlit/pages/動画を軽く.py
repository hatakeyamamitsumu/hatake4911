import streamlit as st
from moviepy.editor import VideoFileClip

def convert_and_display(clip, output_gif, fps=10, resize_percentage=None):
    # 動画サイズ変更
    if resize_percentage:
        resize_factor = resize_percentage / 100.0
        clip = clip.resize(resize_factor)

    # 新しいFPSでGIFに変換
    gif_clip = clip.set_fps(fps)
    gif_clip.write_gif(output_gif)

    # 変換後のGIFを表示
    st.image(output_gif, use_column_width=True)

def main():
    st.title("動画のフレームレートとサイズを変換するアプリ")

    # 動画ファイルのアップロード
    uploaded_file = st.file_uploader("動画ファイルをアップロードしてください", type=["mp4", "avi", "mov"])

    # 動画情報取得
    if uploaded_file is not None:
        clip = VideoFileClip(uploaded_file)
        duration = clip.duration
        st.write(f"動画の長さ: {duration}秒")

        # FPSの入力
        fps = st.slider("変換後のFPSを選択してください", min_value=1, max_value=30, value=10)

        # サイズ変更のスライダー
        resize_percentage = st.slider("動画のサイズを変更する（元の大きさの何％か）", min_value=1, max_value=100, value=100)

        # 変換ボタン
        if st.button("動画を変換して表示"):
            # 出力GIFファイル名
            output_gif_name = "output_animation.gif"

            # 変換処理と表示
            convert_and_display(clip, output_gif_name, fps, resize_percentage)
            st.success("変換が完了しました！")

if __name__ == "__main__":
    main()
