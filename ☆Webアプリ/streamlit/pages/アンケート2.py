import streamlit as st

# ハイパーリンクのURL
link_url = "https://forms.gle/DUHCTT5CfajGjoGMA"
# ハイパーリンクの表示テキスト
link_text = "アンケートにお答えください"

# リンクボタンを作成する関数
def create_link_button(url, text):
    return f'<a href="{url}" target="_blank">{text}</a>'

# ハイパーリンクを含むMarkdown文字列
link_str = f"({link_url})"
# Markdownを表示
st.markdown(link_str, unsafe_allow_html=True)

# リンクボタンを作成して表示
link_button = create_link_button(link_url, link_text)
st.markdown(link_button, unsafe_allow_html=True)
