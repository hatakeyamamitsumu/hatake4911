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

files=os.listdir(folder_path)
opend_imgs=[]
for file in files:
  file_path=os.path.join(folder_path,file)
  image=image.open(file_path)
  opend_imgs.append(image)

imgs=[]
for file in opend_imgs:
  image_bytes=BytesIO()
  file.save(image_bytes,format='PNG')
  encoded=base64.b64encode(image_bytes.getvalue()).decode()
  images.append(f'data:image/png:base64,{encoded}')


clicked=clickable_imagaes(
  images,
  titles=[f'image {fname}' for fname in images],
  div_style={"display":"flex","justify-content":"center","flex-wrap":"wrap"},
  img_style={"margin":"5px","height":"200px",},
)
if clicked<0:
  st.stop()

selected_img_name=[files[clicked][:-4]]
st.write(f'{selected_img_name}に投票しました。')

img_name=[ifle[:-4]for file in files]

for img_names in img_name:
  if img_name not in st.session_state:
    st.session_atate[img_name]=0

st.session_atate[selected_img_name]+=1

save_ss()
count_dict={}
for img_name in img_names:
  count_dict[img_name]=st.session_state[]

df=pd.DataFrame(count_dict,index=['投票数']).T

col1,col2=st.columns(2)
with col1:
  st.write('投票状況')
  st.bar_chart(df)

with col2:
  st.write('構成比')
  fig=go.Figure(
    data=[
      go.Pie(
        labels=df.index,
        values=df["投票数"])
      )
    ]
  fig.update_layout(
    showlegend=True,
    height=290,
    margin={"i":20,"r":60,"t":0,"b":0},
    ),
  fig.update_traces(textposition='inside',textinfo='label+percent')
  st.plotly_chart(fig,use_container_width=True)


def load_ss():
  try:
    with open('session_state.pkl','rb')as f:
      ss_dict=pickle.load(f)
      st.write(pickle.load(f))
      st.write(ss_dict)
      for key in  ss_dict:
        st.session_state[key]=ss_dict[key]
  except FileNotFoundError:
    st.error("指定されたpickleファイルが見つかりませんでした。")
    return None

  st.write('st.session_state')
  st.write(f'{st.session_state}')
def main():
  



  
  


      
      

