import streamlit as st
import MeCab

def perform_morphological_analysis(text):
    mecab = MeCab.Tagger("-Owakati")
    parsed_text = mecab.parse(text)
    return parsed_text

def main():
    st.title("形態素解析アプリ　")
    st.write("テキストファイルをアップロードして形態素解析を行います。")

    uploaded_file = st.file_uploader("テキストファイルを選択してください", type="txt")
    
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        
        result = perform_morphological_analysis(text)
        st.write("形態素解析結果：")
        st.write(result)

        # 解析結果をダウンロードできるボタン
        st.sidebar.download_button(
            label="解析結果をダウンロード",
            data=result,
            file_name="morphological_analysis_result.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
