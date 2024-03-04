import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from pathlib import Path
from typing import List, Dict

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

# データフレーム形式チェック
def is_dataframe(df):
    """
    データフレーム形式かどうかをチェックします。

    Args:
        df: データフレーム

    Returns:
        True: データフレーム形式
        False: データフレーム形式ではない
    """
    return isinstance(df, pd.DataFrame)

# 欠損値処理
def handle_missing_values(df):
    """
    欠損値処理を行います。

    Args:
        df: データフレーム

    Returns:
        df: 欠損値処理済みのデータフレーム
    """
    # 欠損値の割合が50%以下の列のみ処理
    for column in df.columns:
        missing_value_ratio = df[column].isnull().mean()
        if missing_value_ratio <= 0.5:
            # 最頻値で補完
            df[column] = df[column].fillna(df[column].mode())

    return df

# 外れ値処理
def handle_outliers(df):
    """
    外れ値処理を行います。

    Args:
        df: データフレーム

    Returns:
        df: 外れ値処理済みのデータフレーム
    """
    # IQR法を用いて外れ値を除去
    for column in df.columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        df = df[df
