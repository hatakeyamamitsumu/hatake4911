import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
import pickle
from io import BytesIO
import glob
import os
from PIL import Image

st.set_page_config(page_title="投票", layout='wide')


def save_ss():
    ss_dict = {}
    for key in st.session_state:
        ss_dict[key] = st.session_state[key]
    with open('session_state.pkl', 'wb') as f:
        pickle.dump(ss_dict, f)


def set_app():
    def init_all():
        for key in st.session_state.keys():
            del st.session_state[key]
            st.write(f'{key} deleted')

        file_list = glob.glob(os.path.join('/mount/src/hatake4911/☆Webアプリ/streamlit/pages/img', '*'))

        for file_path in file_list:
            try:
                os.remove(file_path)
                st.write(f'Deleted:{file_path}')
            except Exception as e:
                st.write(f'error deleting{file_path}:{e}')

    if st.button('session_state/imgフォルダの初期化'):
        init_all()

    title1 = st.sidebar.text_input('タイトルを入力', key='input_title1')
    st.write(f'title1:{title1}')
    st.session_state['title1'] = title1

    save_ss()
    img_files = st.sidebar.file_uploader('画像pngファイルをアップロード', accept_multiple_files=True)

    if img_files is not None:
        for img_file in img_files:
            with open(f'/mount/src/hatake4911/☆Webアプリ/streamlit/pages/img/{img_file.name}', 'wb') as f:
                f.write(img_file.read())
            st.write(f'{img_file.name} uploaded')


def execute_app():
    if 'title1' not in st.session_state:
        st.info('appの初期設定を行ってください')
        st.stop()

    st.title(st.session_state['title1'])

    st.markdown('投票する画像を選んで下さい')

    folder_path = '/mount/src/hatake4911/☆Webアプリ/streamlit/pages/img'
    files = os.listdir(folder_path)

    for file in files:
        file_path = os.path.join(folder_path, file)
        image = Image.open(file_path)
        st.image(image, caption=f'Image {file}', use_column_width=True)

    clicked = st.button('投票する')

    if clicked:
        st.write(f'投票しました。')


def load_ss():
    try:
        with open('session_state.pkl', 'rb') as f:
            ss_dict = pickle.load(f)
            st.write('pickle.load(f)')
            st.write(ss_dict)
            for key in ss_dict:
                st.session_state[key] = ss_dict[key]
    except FileNotFoundError:
        st.error("指定されたpickleファイルが見つかりませんでした。")
        return None

    st.write('st.session_state')
    st.write(f'{st.session_state}')


def main():
    apps = {
        'appの実行': execute_app,
        'appの初期設定': set_app,
        'pickleファイルから読み込み': load_ss
    }
    selected_app_name = st.sidebar.selectbox(label='項目の選択', options=list(apps.keys()))
    render_func = apps[selected_app_name]
    render_func()


if __name__ == '__main__':
    main()

  



  
  


      
      

