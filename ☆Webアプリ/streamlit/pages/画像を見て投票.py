import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from st_clickable_images import clickable_images
import base64
import pickle
from io import BytesIO
import glob
import os
from PIL import Image

st.set_config(title="投票",layout='wide')
def save_ss():
  ss_dict={}
  for key in st.session_state:
    ss_dict[key]=st.sesion_state[key]
    with open('session_state.pkl','wb') as f:
      pickle.dump(ss_dict.f)

def set_app():
  def init_all():
    for key in st.session_state.keys():
      del st.sesion_state[key]
      st.write(f'{key} deleted')

file_list=glob.glob(os.path.join('img','*'))

for file_path in file_list:
  try:
    os.remove(file_path)
    st.write(f'Deleted:{file_path}')
  except Exception as e:
    st.write(f'error deleting{file_path}:{e}')

if st.bottun('session_state/imgフォルダの初期化'):
  init_all()

title1=st.sidebar.text_input('タイトルを入力',key='input_title1')
st.write(f'title1:{title1}')
st.session_state['title1']=title1

save_ss()
img_files=st.sidebar.file_uploader('画像pngファイルをアップロード',accept_multiple_file)

if img_files is not None:
  for img_file in img_files:
    with open(f'img/{img_file.name}','wb')as f:
      f.write(img_file.read())
    st.write(f'{img_file.name} uploaded')

def execute_app():

  if title1 not in st.session_state:
    st.info('appの初期設定を行ってください')
    st.stop()

st.title(st.session_state['title1'])

st.markdown('投票する画像を選んで下さい')

folder_path='img'
    
      
      

