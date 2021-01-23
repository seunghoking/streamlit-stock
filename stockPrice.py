import streamlit as st
import codeDownload as codeDown
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime, timedelta

st.write('''
# 나만의 주식 데이터
마감 가격과 거래량을 차트로 보여줍니다!
''')

name = st.sidebar.selectbox('회사명', ['삼성전자', '셀트리온', 'NAVER', '카카오', '대한항공','삼성바이오로직스', 'SK하이닉스'])

week = timedelta(weeks=1)
start_date = st.sidebar.date_input('Start date', datetime.now() - week)
end_date = st.sidebar.date_input('End date', datetime.now())

# kospi, kosdaq 종목코드 각각 다운로드
kospi_df = codeDown.get_download_kospi()
kosdaq_df = codeDown.get_download_kosdaq()

# data frame merge
code_df = pd.concat([kospi_df, kosdaq_df])

# data frame정리
code_df = code_df[['회사명', '종목코드']]

# data frame title 변경 '회사명' = name, 종목코드 = 'code'
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

code = codeDown.get_code(code_df, name)

df = pdr.get_data_yahoo(code,start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d'))

st.write('''마감가격''')
st.line_chart(df.Close)
st.write('''거래량''')
st.line_chart(df.Volume)