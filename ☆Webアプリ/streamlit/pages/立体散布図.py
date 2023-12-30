# scatter_plot_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# データベースファイルの読み込み
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# 立体散布図のプロット
def plot_3d_scatter(data, x_col, y_col, z_col):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(data[x_col], data[y_col], data[z_col], c='r', marker='o')
    
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_zlabel(z_col)
    
    st.pyplot(fig)

def main():
    st.title('3D Scatter Plot with Streamlit')
    
    # ファイルのアップロード
    uploaded_file = st.file_uploader('Upload a CSV file', type=['csv'])
    
    if uploaded_file is not None:
        st.write('### Loaded Data:')
        
        # アップロードされたファイルを読み込む
        data = load_data(uploaded_file)
        
        # 列の選択
        selected_columns = st.multiselect('Select columns for 3D Scatter Plot', data.columns)
        
        # 3列が選択された場合にのみ散布図を描画
        if len(selected_columns) == 3:
            st.write('### 3D Scatter Plot:')
            
            # 散布図の描画
            plot_3d_scatter(data, selected_columns[0], selected_columns[1], selected_columns[2])
        else:
            st.warning('Please select exactly 3 columns for the 3D Scatter Plot.')

if __name__ == '__main__':
    main()

