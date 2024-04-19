import streamlit as st
from streamlit.local_storage import LocalStorageType, LocalStorage
local_storage = LocalStorage(LocalStorageType.LOCAL)
user_text = local_storage.get("user_text", "")

# ユーザー入力に基づいて user_text を更新
user_text = st.text_input("テキストを入力してください:", value=user_text)

# 更新された user_text をローカルストレージに保存
local_storage.set("user_text", user_text)
