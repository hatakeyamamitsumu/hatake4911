import streamlit as st
from moviepy.editor import VideoFileClip

def convert_video_to_gif(input_file, output_file, fps=10, target_size=None):
    clip = VideoFileClip(input_file)

    # 動画サイズ変更
    if target_size:
        clip = clip.resize(target_size)

    clip.write_gif(output_file, fps=fps)

def main():
    st.title("動画をGIFに変換するアプリ")

    # 動画ファイルのアップロード
    uploaded_file = st.file_uploader("動画ファイルをアップロードしてください", type=["mp4", "avi", "mov"])

    if uploaded_file is not None:
        # 出力GIFファイル名の入力
        output_gif_name = st.text_input("出力GIFファイル名を入力してください", "output_animation.gif")

        # FPSの入力
        fps = st.slider("変換するGIFのフレームレートを選択してください", min_value=1, max_value=30, value=10)

        # 動画サイズ変更の設定
        resize_option = st.checkbox("動画のサイズを変更する", value=False)
        if resize_option:
            width = st.number_input("変更後の幅を入力してください", min_value=1)
            height = st.number_input("変更後の高さを入力してください", min_value=1)
            target_size = (width, height)
        else:
            target_size = None

        # 変換ボタン
        if st.button("動画をGIFに変換"):
            # 変換処理
            convert_video_to_gif(uploaded_file, output_gif_name, fps, target_size)
            st.success("変換が完了しました！")

            # 変換後のGIFを表示
            st.image(output_gif_name, use_column_width=True)

if __name__ == "__main__":
    main()
