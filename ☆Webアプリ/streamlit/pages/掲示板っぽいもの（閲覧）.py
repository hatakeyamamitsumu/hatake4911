import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd

SP_CREDENTIAL_FILE = '/mount/src/hatake4911/☆Webアプリ/秘密鍵/gspread-test-421301-6cd8b0cc0e27.json'

SP_SCOPE = [
    'https://www.googleapis.com/auth/drive',
    'https://spreadsheets.google.com/feeds'
]
SP_SHEET_KEY = '1GuaN72pbZxQJBsxLTK3n7fAQfLMJIcuUjZ7pBd-R7kc'

# ユーザーが選択するシートのリスト
AVAILABLE_SHEETS = ['話題1', '話題2', '話題3']  # これを必要に応じて変更してください

# 選択式を作成する
print("選択してください:")
for i, sheet in enumerate(AVAILABLE_SHEETS, start=1):
    print(f"{i}. {sheet}")

selection = int(input("番号を入力してください: "))  # ユーザーの選択を受け付ける

# ユーザーの選択に基づいてSP_SHEETを設定
SP_SHEET = AVAILABLE_SHEETS[selection - 1]

credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, SP_SCOPE)
gc = gspread.authorize(credentials)
sh = gc.open_by_key(SP_SHEET_KEY)
worksheet = sh.worksheet(SP_SHEET)
data = worksheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

print(df)

