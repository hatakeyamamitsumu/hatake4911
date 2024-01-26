import streamlit as st
import pandas as pd
import io
import base64

st.set_page_config(page_title='簡易見積app')
st.title('簡易見積app')

df = pd.DataFrame(
    [
        {'商品名': 'Tシャツ-白', '単価': 1000},
        {'商品名': 'Tシャツ-黒', '単価': 1000},
        {'商品名': 'Tシャツ-白犬', '単価': 1300},
        {'商品名': 'Tシャツ-黒猫', '単価': 1300},
        {'商品名': 'パーカー-白', '単価': 3000},
        {'商品名': 'パーカー-黒', '単価': 3000},
        {'商品名': 'Yシャツ-白', '単価': 2500},
        {'商品名': 'Yシャツ-ストライプ', '単価': 3000},
        {'商品名': 'トレーナー-グレー', '単価': 2000},
        {'商品名': 'トレーナー-黒', '単価': 2000},
    ]
)

with st.expander('カタログを開く', expanded=False):
    st.dataframe(df)

def calculate_subtotal(item, quantity):
    selected_df = df[df['商品名'] == item]
    selected_df['数量'] = quantity
    selected_df['小計'] = selected_df['単価'] * selected_df['数量']
    return selected_df

# 商品名リストの作成
items = df['商品名'].unique()
items = sorted(items)
items.insert(0, '--商品名を選択--')

# 複数の見積もりを処理
estimates = []
for i in range(1, 20):  # 最大で20の見積もりを許可（必要に応じて調整してください）
    st.sidebar.markdown(f'#### 見積{i}')
    selected_item = st.sidebar.selectbox(f'商品名{i}:', items, key=f'selected_item{i}')

    if selected_item == '--商品名を選択--':
        break  # 商品が選択されていない場合は終了

    cnt = st.sidebar.number_input(f'数量入力{i}', min_value=0, max_value=10, key=f'cnt{i}')

    df_estimate = calculate_subtotal(selected_item, cnt)
    estimates.append(df_estimate)

# 見積もりを表示
if estimates:
    st.subheader('見積詳細')
    total_estimate = pd.concat(estimates, ignore_index=True)
    st.dataframe(total_estimate)

    # 合計金額を計算して表示
    total_price = total_estimate['小計'].sum()
    st.markdown(f'**合計金額:** {total_price} 円')

    # 合計金額をtotal_estimateに追加
    total_estimate.loc[len(total_estimate.index)] = ['合計', '', '', total_price]

    # 見積もりをCSVファイルに保存
    if st.button('見積をCSVファイルでダウンロードしますか？'):
        csv_file = total_estimate.to_csv(index=False, encoding='utf-8-sig')
        b64 = base64.b64encode(csv_file.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="estimate.csv">ここをクリックしてダウンロードしてください</a>'
        st.markdown(href, unsafe_allow_html=True)



