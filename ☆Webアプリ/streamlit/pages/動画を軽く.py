import streamlit as st
from moviepy.editor import VideoFileClip

def convert_and_display(clip, fps=10, resize_percentage=None):
    # 動画サイズ変更
    if resize_percentage:
        resize_factor = resize_percentage / 100.0
        clip = clip.resize(resize_factor)

    # 新しいFPSで動画を再エンコード
    new_clip = clip.set_fps(fps)

    # 変換後の動画を表示
    st.video(new_clip.write_to_memory(fps=fps), format="video/mp4")

def main():
    st.title("動画のフレームレートとサイズを変更するアプリ")

    # 動画ファイルのアップロード
    uploaded_file = st.file_uploader("動画ファイルをアップロードしてください", type=["mp4", "avi", "mov"])

    # 動画情報取得
    if uploaded_file is not None:
        # 動画ファイルかどうかを確認
        if uploaded_file.type.startswith('video'):
            # 動画ファイルをメモリに読み込む
            video_bytes = uploaded_file.read()
            clip = VideoFileClip(video_bytes, codec="libx264", audio_codec="aac")

            duration = clip.duration
            st.write(f"動画の長さ: {duration}秒")

            # FPSの入力
            fps = st.slider("変換後のFPSを選択してください", min_value=1, max_value=30, value=10)

            # サイズ変更のスライダー
            resize_percentage = st.slider("動画のサイズを変更する（元の大きさの何％か）", min_value=1, max_value=100, value=100)

            # 変換ボタン
            if st.button("動画を変換して表示"):
                # 変換処理と表示
                convert_and_display(clip, fps, resize_percentage)
                st.success("変換が完了しました！")
        else:
            st.error("サポートされていない動画ファイル形式です。対応する形式をアップロードしてください。")

if __name__ == "__main__":
    main()
