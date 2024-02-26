import streamlit as st
# ハイパーリンクを表示するMarkdown文字列
link_str = "(https://forms.gle/DUHCTT5CfajGjoGMA)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('↑アンケートにお答えください。')





# リンクボタンを作成する関数
def create_link_button(url, text):
    return f'<a href="{url}" target="_blank">{text}</a>'

# Streamlitアプリケーション
def main():
    st.title("リンクボタンの例")

    # リンクURL
    link_url = "https://forms.gle/DUHCTT5CfajGjoGMA"

    # リンクボタンを作成
    link_button = create_link_button(link_url, "アンケートに移動する")

    # HTMLを表示
    st.markdown(link_button, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
