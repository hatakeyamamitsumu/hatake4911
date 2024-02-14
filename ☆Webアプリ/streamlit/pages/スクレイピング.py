import streamlit as st
from googlesearch import search
import time

def google_search(keyword, num_results):
    url_list = []
    with st.spinner("検索中..."):
        for url in search(keyword, lang='jp', num_results=num_results):
            url_list.append(url)
            time.sleep(2)  # ページ間の適切な待機時間（2秒）に変更
    return url_list

def main():
    st.title('Google検索結果表示ページ')

    keyword = st.text_input('検索キーワードを入力してください', '山 海 魚')
    num_results = st.slider('表示する結果の数', min_value=1, max_value=20, value=10)

    if st.button('検索開始'):
        results = google_search(keyword, num_results)
        
        st.write(f'### 検索結果 ({len(results)} 件):')
        for i, url in enumerate(results, start=1):
            st.text(f"{i}. {url}")

if __name__ == '__main__':
    main()
