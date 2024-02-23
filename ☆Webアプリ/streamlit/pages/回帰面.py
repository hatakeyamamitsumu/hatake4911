# scatter_plot_app.py

import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file_path, encoding):
    data = pd.read_csv(file_path, encoding=encoding)
    return data

def plot_3d_scatter_with_trendline(data, x_col, y_col, z_col, index_col):
    fig = px.scatter_3d(data, x=x_col, y=y_col, z=z_col, text=index_col, trendline="ols")
    st.plotly_chart(fig)

def plot_2d_scatter_with_trendline(data, x_col, y_col, index_col):
    fig = px.scatter(data, x=x_col, y=y_col, text=index_col, trendline="ols")
    st.plotly_chart(fig)

def plot_scatter_with_trendline(data, selected_columns, index_col, dimensions):
    if dimensions == 2:
        plot_2d_scatter_with_trendline(data, selected_columns[0], selected_columns[1], index_col)
    elif dimensions == 3:
        plot_3d_scatter_with_trendline(data, selected_columns[0], selected_columns[1], selected_columns[2], index_col)

def main():
    st.title('散布図表示ページ')
    st.text('インデックスの多すぎるファイルは見づらくなります。')

    uploaded_file_utf8 = st.file_uploader('3列以上あるＣＳＶデータベースファイルをアップロードしてください (UTF-8)', type=['csv'])
    uploaded_file_shiftjis = st.file_uploader('3列以上あるＣＳＶデータベースファイルをアップロードしてください  (Shift-JIS)', type=['csv'])

    if uploaded_file_utf8 is not None or uploaded_file_shiftjis is not None:
        st.write('### Loaded Data:')

        if uploaded_file_utf8 is not None:
            data_utf8 = load_data(uploaded_file_utf8, encoding='utf-8')
            selected_columns_utf8 = st.multiselect('散布図用の列を選んでください', data_utf8.columns)

            if len(selected_columns_utf8) >= 2 and len(selected_columns_utf8) <= 3:
                index_col_utf8 = st.selectbox('見出し列を選んでください（見出し数が10程度の表がおすすめです）', data_utf8.columns)
                dimensions_utf8 = len(selected_columns_utf8)
                st.write(f'### {dimensions_utf8}次元散布図 (UTF-8):')
                plot_scatter_with_trendline(data_utf8, selected_columns_utf8, index_col_utf8, dimensions_utf8)
            else:
                st.warning('2列または３列のみ選択してください。.')

        if uploaded_file_shiftjis is not None:
            data_shiftjis = load_data(uploaded_file_shiftjis, encoding='shift-jis')
            selected_columns_shiftjis = st.multiselect('散布図用の列を選んでください', data_shiftjis.columns)

            if len(selected_columns_shiftjis) >= 2 and len(selected_columns_shiftjis) <= 3:
                index_col_shiftjis = st.selectbox('見出し列を選んでください（見出し数が10程度の表がおすすめです）', data_shiftjis.columns)
                dimensions_shiftjis = len(selected_columns_shiftjis)
                st.write(f'### {dimensions_shiftjis}次元散布図 (Shift-JIS):')
                plot_scatter_with_trendline(data_shiftjis, selected_columns_shiftjis, index_col_shiftjis, dimensions_shiftjis)
            else:
                st.warning('Please select 2 or 3 columns for the Scatter Plot.')

if __name__ == '__main__':
    main()
