import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels

def load_data(file_path, encoding):
    data = pd.read_csv(file_path, encoding=encoding)
    return data

def plot_scatter(data, selected_columns, index_col, dimensions):
    if dimensions == 2:
        # 2D Scatter Plot with Trendline
        fig = px.scatter(data, x=selected_columns[0], y=selected_columns[1], text=index_col, trendline="ols")
        st.plotly_chart(fig)
    elif dimensions == 3:
        # 3D Scatter Plot with Regression Plane
        fig = px.scatter_3d(data, x=selected_columns[0], y=selected_columns[1], z=selected_columns[2], text=index_col, trendline="ols")
        st.plotly_chart(fig)

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

            if 2 <= len(selected_columns_utf8) <= 3:
                index_col_utf8 = st.selectbox('見出し列を選んでください（見出し数が10程度の表がおすすめです）', data_utf8.columns)
                dimensions_utf8 = len(selected_columns_utf8)
                st.write(f'### {dimensions_utf8}D Scatter Plot (UTF-8):')
                plot_scatter(data_utf8, selected_columns_utf8, index_col_utf8, dimensions_utf8)
            else:
                st.warning('2つか3つの列を選択してください。')

        if uploaded_file_shiftjis is not None:
            data_shiftjis = load_data(uploaded_file_shiftjis, encoding='shift-jis')
            selected_columns_shiftjis = st.multiselect('散布図用の列を選んでください', data_shiftjis.columns)

            if 2 <= len(selected_columns_shiftjis) <= 3:
                index_col_shiftjis = st.selectbox('見出し列を選んでください（見出し数が10程度の表がおすすめです）', data_shiftjis.columns)
                dimensions_shiftjis = len(selected_columns_shiftjis)
                st.write(f'### {dimensions_shiftjis}D Scatter Plot (Shift-JIS):')
                plot_scatter(data_shiftjis, selected_columns_shiftjis, index_col_shiftjis, dimensions_shiftjis)
            else:
                st.warning('2つか3つの列を選択してください。')

if __name__ == '__main__':
    main()
