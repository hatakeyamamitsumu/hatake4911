import streamlit as st
import pandas as pd
import io
import openpyxl

# pip install streamlit pandas openpyxl

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

with st.expander('df', expanded=False):
    st.dataframe(df)

#商品名リストの作成
items = df['商品名'].unique()
items = sorted(items)

#リストに1行目を挿入　すぐに見積もりが始まらないように
items.insert(0, '--商品名を選択--')

####################1行目
# 商品名選択
st.sidebar.markdown('#### 見積1')
selected_item = st.sidebar.selectbox('商品名:',items, key='selected_item1')

df1 = df[df['商品名']==selected_item]

# 数量入力
cnt1 = st.sidebar.number_input('数量入力', min_value=0, max_value=10, key='cnt1')

df1['数量'] = cnt1
df1['小計'] = df1['単価'] * df1['数量']
