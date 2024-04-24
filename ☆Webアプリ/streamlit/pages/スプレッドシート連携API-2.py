import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets 認証情報のファイルパスとスコープ
SP_CREDENTIAL_FILE = '/mount/src/hatake4911/☆Webアプリ/streamlit/gspread-test-421301-6cd8b0cc0e27.json'
SP_SCOPE = ['https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds']
SP_SHEET_KEY = '1GuaN72pbZxQJBsxLTK3n7fAQfLMJIcuUjZ7pBd-R7kc'
SP_SHEET_NAME = 'DEMO'

# 認証情報の読み込みと認証
credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, SP_SCOPE)
gc = gspread.authorize(credentials)

# スプレッドシートの指定
sh = gc.open_by_key(SP_SHEET_KEY)
worksheet = sh.worksheet(SP_SHEET_NAME)

# 表の列数を取得
num_columns = len(worksheet.row_values(1))

# ユーザーにデータの入力を求めるループ
while True:
    # データの入力を求める
    new_data = input("新しいデータを入力してください (終了するには 'exit' と入力): ")
    
    # 入力が 'exit' ならばループを終了
    if new_data.lower() == 'exit':
        print("終了します。")
        break
    
    # 入力されたデータをリストに分割
    new_data_list = new_data.split(',')
    
    # 入力されたデータの列数が表の列数と一致するかチェック
    if len(new_data_list) != num_columns:
        print("入力されたデータの列数が不正です。正しい列数のデータを入力してください。")
        continue
    
    # スプレッドシートにデータを書き込む
    worksheet.append_row(new_data_list)
    print("データをスプレッドシートに書き込みました。")
