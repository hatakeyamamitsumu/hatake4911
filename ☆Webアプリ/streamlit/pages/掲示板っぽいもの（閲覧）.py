import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd
from ipywidgets import interact, widgets

SP_CREDENTIAL_FILE = '/mount/src/hatake4911/☆Webアプリ/秘密鍵/gspread-test-421301-6cd8b0cc0e27.json'

SP_SCOPE = [
    'https://www.googleapis.com/auth/drive',
    'https://spreadsheets.google.com/feeds'
]
SP_SHEET_KEY = '1GuaN72pbZxQJBsxLTK3n7fAQfLMJIcuUjZ7pBd-R7kc'

# Google Sheetsからシート名を取得する関数
def get_sheet_names(credentials, sheet_key):
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(sheet_key)
    return [worksheet.title for worksheet in sh.worksheets()]

# 選択式のセレクトボックスを作成する関数
def select_sheet(sheet_names):
    @interact(sheet_name=sheet_names)
    def get_selected_sheet(sheet_name):
        return sheet_name

# シート名の取得とセレクトボックスの表示
credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, SP_SCOPE)
sheet_names = get_sheet_names(credentials, SP_SHEET_KEY)
select_sheet(sheet_names)
