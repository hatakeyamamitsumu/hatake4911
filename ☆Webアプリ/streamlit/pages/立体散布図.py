# scatter_plot_app.py

import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def plot_3d_scatter(data, x_col, y_col, z_col):
    fig = px.scatter_3d(data, x=x_col, y=y_col, z=z_col)
    st.plotly_chart(fig)

def main():
    st.title('3D Scatter Plot with Streamlit')
    
    uploaded_file = st.file_uploader('Upload a CSV file', type=['csv'])
    
    if uploaded_file is not None:
        st.write('### Loaded Data:')
        
        data = load_data(uploaded_file)
        
        selected_columns = st.multiselect('Select columns for 3D Scatter Plot', data.columns)
        
        if len(selected_columns) == 3:
            st.write('### 3D Scatter Plot:')
            plot_3d_scatter(data, selected_columns[0], selected_columns[1], selected_columns[2])
        else:
            st.warning('Please select exactly 3 columns for the 3D Scatter Plot.')

if __name__ == '__main__':
    main()

