import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from pathlib import Path

# ファイル形式の自動判別
def detect_encoding(uploaded_file):
    """
    アップロードされたファイルのエンコードを判別します。

    Args:
        uploaded_file: アップロードされたファイル

    Returns:
        エンコード
    """
    # 最初の数バイトを読み込み
    file_bytes = uploaded_file.read(n=3)
    # UTF-8 BOMのチェック
    if file_bytes.startswith(b'\xef\xbb\xbf'):
        return 'utf-8'
    # Shift-JIS BOMのチェック
    elif file_bytes.startswith(b'\x81\x43'):
        return 'shift-jis'
    # その他
    else:
        return 'utf-8'

# グラフ設定
def plot_settings(df, selected_columns):
    """
    グラフ設定を行います。

    Args:
        df: データフレーム
        selected_columns: 選択された列

    Returns:
        fig: グラフ
    """
    # グラフ作成
    fig, ax1 = plt.subplots()

    # 日ごとの選択された列を含む新しいデータフレームを作成
    df_selected_columns = df[selected_columns]

    # データを共有するための共通の軸を作成
    for i, column in enumerate(selected_columns):
        # 異なる色を使いたい場合、以下のように指定します
        color = plt.cm.viridis(i / len(selected_columns))

        # 軸ラベル設定
        ax1.set_xlabel('---')
        ax1.set_ylabel(column, color=color)

        # 折れ線グラフ作成
        ax1.plot(df.index, df_selected_columns[column], label=column, color=color)

        # 軸ラベルの色設定
        ax1.tick_params(axis='y', labelcolor=color)

    # グラフタイトル設定
    ax1.set_title('グラフタイトル')

    # 凡例設定
    ax1.legend(loc='upper left', bbox_to_anchor=(1, 1))

    return fig

# メイン処理
st.set_page_config(page_title='csvファイル', layout='centered')

# 複数ファイルアップロード
uploaded_files = st.file_uploader('CSVファイル', type='csv', accept_multiple_files=True)

# ファイル処理
for uploaded_file in uploaded_files:
    # ファイル名
    file_name = uploaded_file.name

    # エンコード自動判別
    encoding = detect_encoding(uploaded_file)

    # データフレーム読み込み
    try:
        df = pd.read_csv(uploaded_file, encoding=encoding)

        # データフレーム形式チェック
        if isinstance(df, pd.DataFrame):
            # データフレーム形式の場合
            # 列選択
            selected_columns = st.multiselect(f"{file_name} - グラフ化したい列を選択してください。（取り込んだファイルがデータベース形式である場合に限られます）", df.columns)

            # グラフ設定
            fig = plot_settings(df, selected_columns)

            # グラフ表示
            st.pyplot(fig)
        else:
            # データフレーム形式ではない場合
            st.error(f"{file_name} - データフレーム形式ではないため、グラフ化できません。")

    except Exception as e:
        st.error(f"{file_name} - エラー: {str(e)}")

# ファイルダウンロード
if st.button('ダウンロード'):
    # ダウンロード用ファイル名
    download_file_name = 'download.csv'

    # CSVファイル形式に変換
    csv_string = df.to_csv(index=False)

    # ファイルオブジェクト作成
    file_object = io.StringIO(csv_string)

    # ダウンロード処理
    st.download_button(label='ダウンロード', data=file_object, file_name=download_file_name, mime='text/csv')

# データ保存・読み込み
if st.button('保存'):
    # 保存データ
