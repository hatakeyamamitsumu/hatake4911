from PIL import Image
import pandas as pd
import plotly.graph_objects as go
import sqlite3

# データベースへの接続
conn = sqlite3.connect('app_data.db')
c = conn.cursor()

# テーブルが存在しない場合は作成
c.execute('''
    CREATE TABLE IF NOT EXISTS session_data (
        key TEXT PRIMARY KEY,
        value TEXT
    )
''')

st.set_page_config(page_title="投票", layout='wide')

@@ -13,13 +26,16 @@ def save_ss():
        ss_dict[key] = st.session_state[key]

    try:
        # pickle ファイルのパスを修正
        file_path = 'https://raw.githubusercontent.com/hatakeyamamitsumu/hatake4911/main/session_state.pkl'
        with st.cache(allow_output_mutation=True):
            with open(file_path, 'wb') as f:
                pickle.dump(ss_dict, f)
        # データベースに保存
        for key, value in ss_dict.items():
            c.execute('''
                INSERT OR REPLACE INTO session_data (key, value)
                VALUES (?, ?)
            ''', (key, str(value)))

        conn.commit()
    except Exception as e:
        st.error(f"ファイルへの書き込み中にエラーが発生しました: {e}")
        st.error(f"データベースへの書き込み中にエラーが発生しました: {e}")


def set_app():
@@ -121,20 +137,23 @@ def execute_app():

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
        # データベースから読み込み
        c.execute('SELECT key, value FROM session_data')
        rows = c.fetchall()

        ss_dict = {}
        for row in rows:
            key, value = row
            ss_dict[key] = value

        st.write('データベースから読み込み成功')
        st.write(ss_dict)

        # st.session_state にセット
        for key in ss_dict:
            st.session_state[key] = ss_dict[key]
    except Exception as e:
        st.error(f"ファイルの読み込み中にエラーが発生しました: {e}")
        st.error(f"データベースからの読み込み中にエラーが発生しました: {e}")

    st.write('st.session_state')
    st.write(st.session_state)
@@ -144,7 +163,7 @@ def main():
    apps = {
        'appの実行': execute_app,
        'appの初期設定': set_app,
        'pickleファイルから読み込み': load_ss
        'データベースから読み込み': load_ss
    }
    selected_app_name = st.sidebar.selectbox(label='項目の選択', options=list(apps.keys()))
    render_func = apps[selected_app_name]
@@ -153,3 +172,4 @@ def main():

if __name__ == '__main__':
    main()
