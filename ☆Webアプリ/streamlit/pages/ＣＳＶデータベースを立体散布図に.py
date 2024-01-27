# scatter_plot_app.py

import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file_path, encoding):
    data = pd.read_csv(file_path, encoding=encoding)
    return data

def plot_3d_scatter(data, x_col, y_col, z_col, index_col):
    fig = px.scatter_3d(data, x=x_col, y=y_col, z=z_col, text=index_col)
    st.plotly_chart(fig)

def main():
    st.title('3D 散布図表示ページ')
    st.text('インデックスの多すぎるファイルは見づらくなります。')
    
    uploaded_file_utf8 = st.file_uploader('3列以上あるＣＳＶデータベースファイルをアップロードしてください (UTF-8)', type=['csv'])
    uploaded_file_shiftjis = st.file_uploader('3列以上あるＣＳＶデータベースファイルをアップロードしてください  (Shift-JIS)', type=['csv'])
    
    if uploaded_file_utf8 is not None or uploaded_file_shiftjis is not None:
        st.write('### Loaded Data:')
        
        if uploaded_file_utf8 is not None:
            data_utf8 = load_data(uploaded_file_utf8, encoding='utf-8')
            selected_columns_utf8 = st.multiselect('3D 散布図用の列を選んでください', data_utf8.columns)
            
            if len(selected_columns_utf8) == 3:
                index_col_utf8 = st.selectbox('見出し列を選んでください（見出し数が10程度の表がおすすめです）', data_utf8.columns)
                st.write('### 3D Scatter Plot (UTF-8):')
                plot_3d_scatter(data_utf8, selected_columns_utf8[0], selected_columns_utf8[1], selected_columns_utf8[2], index_col_utf8)
            else:
                st.warning('Please select exactly 3 columns for the 3D Scatter Plot.')

        if uploaded_file_shiftjis is not None:
            data_shiftjis = load_data(uploaded_file_shiftjis, encoding='shift-jis')
            selected_columns_shiftjis = st.multiselect('Select columns for 3D Scatter Plot', data_shiftjis.columns)
            
            if len(selected_columns_shiftjis) == 3:
                index_col_shiftjis = st.selectbox('Select the index column for labels', data_shiftjis.columns)
                st.write('### 3D Scatter Plot (Shift-JIS):')
                plot_3d_scatter(data_shiftjis, selected_columns_shiftjis[0], selected_columns_shiftjis[1], selected_columns_shiftjis[2], index_col_shiftjis)
            else:
                st.warning('Please select exactly 3 columns for the 3D Scatter Plot.')

if __name__ == '__main__':
    main()

