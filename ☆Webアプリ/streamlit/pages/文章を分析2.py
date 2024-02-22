def filter_and_download(text, filter_type):
    if filter_type == 'katakana':
        filtered_lines = filter_katakana(text)
        result_label = "### カタカナを含む行のリスト"
        file_extension = "txt"
    elif filter_type == 'numbers':
        filtered_lines = filter_numbers(text)
        result_label = "### 数字（漢数字を含む）を含む行のリスト"
        file_extension = "txt"
    elif filter_type == 'alphabets':
        filtered_lines = filter_alphabets(text)
        result_label = "### アルファベットを含む行のリスト"
        file_extension = "txt"
    else:
        st.error("無効なフィルタータイプが選択されました。")
        return

    if filtered_lines:
        result_text = "\n".join(filtered_lines)
        st.write(result_label)
        st.text(result_text)

        # Save the filtered lines to a text file
        file_name = f"{filter_type}_data.{file_extension}"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(result_text)

        st.download_button(label="テキストファイルとしてダウンロード", data=result_text, file_name=file_name, key=f"{filter_type}_download_button")
    else:
        st.write(f"テキストに対象の行は見つかりませんでした。")
