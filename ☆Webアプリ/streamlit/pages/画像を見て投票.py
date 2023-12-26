from PIL import Image
import pandas as pd
import plotly.graph_objects as go
import sqlite3
import streamlit as st
import pickle
import os  # 追加
# データベースへの接続
db_path = 'app_data.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# テーブルが存在しない場合は作成
c.execute('''
    CREATE TABLE IF NOT EXISTS session_data (
        key TEXT PRIMARY KEY,
        value TEXT
    )
''')
conn.commit()

st.set_page_config(page_title="投票", layout='wide')

def save_ss():
    ss_dict = {}
    for key in st.session_state:
        ss_dict[key] = st.session_state[key]
    
    try:
        # データベースに保存
        for key, value in ss_dict.items():
            c.execute('''
                INSERT OR REPLACE INTO session_data (key, value)
                VALUES (?, ?)
            ''', (key, str(value)))
        
        conn.commit()
    except Exception as e:
        st.error(f"データベースへの書き込み中にエラーが発生しました: {e}")

def set_app():
    def init_all():
        for key in st.session_state.keys():
            del st.session_state[key]
            st.write(f'{key} deleted')

        folder_path = '/mount/src/hatake4911/☆Webアプリ/streamlit/pages/img'
        files = os.listdir(folder_path)

        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            try:
                os.remove(file_path)
                st.write(f'Deleted: {file_path}')
            except Exception as e:
                st.write(f'Error deleting {file_path}: {e}')

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

    # 画像を選択するためのセレクトボックス
    selected_img_name = st.selectbox('画像を選んでください', files)

    image_path = os.path.join(folder_path, selected_img_name)
    image = Image.open(image_path)
    st.image(image, caption=f'Image {selected_img_name}', use_column_width=True)

    clicked = st.button('投票する')

    if clicked:
        # 選択された画像名を保存
        st.session_state['selected_img_name'] = selected_img_name

        # 投票数を更新
        if selected_img_name not in st.session_state:
            st.session_state[selected_img_name] = 0
        st.session_state[selected_img_name] += 1

        st.write(f'{selected_img_name}に投票しました。')

        # 投票結果を表示
        count_dict = {}
        for img_name in files:
            count_dict[img_name] = st.session_state.get(img_name, 0)

        df = pd.DataFrame(count_dict, index=['投票数']).T

        col1, col2 = st.columns(2)

        with col1:
            st.write('投票状況')
            st.bar_chart(df)

        with col2:
            st.write('構成比')
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=df.index,
                        values=df["投票数"]
                    )])

            fig.update_layout(
                showlegend=True,
                height=290,
                margin={"l": 20, "r": 60, "t": 0, "b": 0},
            )
            fig.update_traces(textposition='inside', textinfo='label+percent')
            st.plotly_chart(fig, use_container_width=True)

def load_ss():
    try:
        # pickle ファイルのパスを修正
        file_path = 'https://raw.githubusercontent.com/hatakeyamamitsumu/hatake4911/main/session_state.pkl'
        with st.cache(allow_output_mutation=True):
            with open(file_path, 'rb') as f:
                ss_dict = pickle.load(f)
                st.write('pickle.load(f)')
                st.write(ss_dict)
                for key in ss_dict:
                    st.session_state[key] = ss_dict[key]
    except FileNotFoundError:
        st.error("指定された pickle ファイルが見つかりませんでした。")
        return None

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
