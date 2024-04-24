import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

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

# 現在のデータ取得
data = worksheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

# 追加するデータ
new_data = [
    ["新しいデータ1", "新しいデータ2", "新しいデータ3", "新しいデータ4"],
    ["さらに追加されたデータ1", "さらに追加されたデータ2", "さらに追加されたデータ3", "さらに追加されたデータ4"]
]

# 新しいデータを追加
new_data_df = pd.DataFrame(new_data, columns=df.columns)
updated_df = pd.concat([df, new_data_df], ignore_index=True)

# 新しいデータをスプレッドシートに書き込み
worksheet.update([updated_df.columns.values.tolist()] + updated_df.values.tolist())

print("新しいデータをスプレッドシートに書き込みました。")
