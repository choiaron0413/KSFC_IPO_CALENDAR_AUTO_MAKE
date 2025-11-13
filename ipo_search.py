#!/usr/bin/env python
# coding: utf-8

# # 중복청약 IPO 캘린더

# ### 1. 조회기간 입력

import pandas as pd
from IPython.display import display
import requests
from bs4 import BeautifulSoup as bs
import os
import streamlit as st
from openpyxl import Workbook
import time
from datetime import datetime
from calendarUtils import set_title, set_weeks_title, set_ipo_calendar



# ### 2. 38커뮤니케이션 IPO 일정 스크래핑
def scrawl_ipo_schedule():
    itr_flag=True
    ipo_df_f=None

    pge_cnt=1
    while True == itr_flag :
        url_list = "http://www.38.co.kr/html/fund/index.htm?o=k&page={0}"
        url = url_list.format(pge_cnt)
        print(url)
        response = requests.get(url)
        soup=bs(response.text, 'html.parser')
        ipo_talbe_tag=soup.find('table', summary="공모주 청약일정")
        #pprint(ipo_talbe_tag)
        
        ipo_df=pd.read_html(str(ipo_talbe_tag))[0]
        ipo_df=ipo_df.iloc[:,0:6]
        
        ipo_df=ipo_df[['종목명','공모주일정','주간사']]
        ipo_df['청약시작일자']=ipo_df['공모주일정'].str.split('~').str[0]
        ipo_df['청약종료일자']=ipo_df['공모주일정'].str.split('~').str[1]
        ipo_df['청약종료일자']=ipo_df['청약시작일자'].str.slice(0,5)+ipo_df['청약종료일자']
        ipo_df=ipo_df[['종목명','청약시작일자','청약종료일자','주간사']]
        #print(ipo_df.head(10))
        
        ipo_df['청약시작일자']=ipo_df['청약시작일자'].str.replace(pat='.', repl='-', regex=False)
        ipo_df['청약종료일자']=ipo_df['청약종료일자'].str.replace(pat='.', repl='-', regex=False)
        
        ipo_df.loc[True==ipo_df['종목명'].str.contains('\(유가\)'),['시장']]='유가증권시장'
        ipo_df.loc[False==ipo_df['종목명'].str.contains('\(유가\)'),['시장']]='코스닥'
        ipo_df['종목명']=ipo_df['종목명'].str.replace(pat='\(유가\)', repl='', regex=True)
        
        ipo_df=ipo_df[['종목명','시장','청약시작일자','청약종료일자','주간사']]
        
        if ipo_df_f is None :
            ipo_df_f=ipo_df
        else :
            ipo_df_f=pd.concat([ipo_df_f, ipo_df],ignore_index=True)
        

        display( ipo_df_f.tail(10) )
        
        if 10 == pge_cnt :
            itr_flag = False
        else :
            pge_cnt=pge_cnt+1
        
        time.sleep(2) # sleep 2 sec
    return ipo_df_f

# ### 3. 인수회사 2개 이상인 종목만 필터링
def filter_ipo_schedule(ipo_df_f):
    ipo_df_f=ipo_df_f.loc[True == ipo_df_f['주간사'].str.contains(',')]#인수회사가 2개 이상인 경우만 취합
    return ipo_df_f


# ### 4. 조회기간 필터 적용

# In[5]:

def filter_ipo_by_inq_dt(ipo_df_f, inq_st_dt, inq_nd_dt):
    # 1. '청약종료일자' 열을 datetime 객체로 변환하고, date 객체만 추출하여 Series로 만듭니다.
    #    이렇게 하면 inq_st_dt (date 객체)와 직접 비교가 가능해집니다.
    ipo_end_dt_series = pd.to_datetime(ipo_df_f['청약종료일자'], errors='coerce').dt.date

    # 2. 필터링 조건에서 변환된 Series를 사용하여 자료형을 맞춰 비교합니다.
    ipo_df_f = ipo_df_f.loc[
        (
            # inq_st_dt (date) <= ipo_end_dt_series (Series of date)
            ( inq_st_dt <= ipo_end_dt_series ) 
            &
            # ipo_end_dt_series (Series of date) <= inq_nd_dt (date)
            ( ipo_end_dt_series <= inq_nd_dt ) 
        )
    ]

    # Streamlit 출력 함수는 유지
    st.dataframe(ipo_df_f)
    # 참고: st.date_input은 Python의 datetime.date 객체를 반환합니다.
    return ipo_df_f


# ### 5. 중복청약확인 대상 종목정보 엑셀파일로 저장
def save_ipo_schedule_to_excel(ipo_df_f, inq_st_dt, inq_nd_dt):
    # output 디렉토리 생성
    os.makedirs("./output/", exist_ok=True)
    
    # 🚨 수정된 부분: 날짜 객체를 문자열로 변환하고 f-string을 사용하여 파일 이름 생성
    file_name = f"./output/ipo_schedule_{inq_st_dt.isoformat()}_{inq_nd_dt.isoformat()}.xlsx"

    ipo_df_f.to_excel(
        file_name  # 디렉토리와 파일 이름 (이제 문자열입니다)
        , sheet_name = 'Sheet1'
        , na_rep = 'NaN'
        , header = True
        , index = False
        , startrow = 1
        , startcol = 1
        , freeze_panes = (2, 0)
    ) 
    
    # 저장된 파일 이름을 출력하여 확인 (선택 사항)
    print(f"데이터가 다음 파일에 저장되었습니다: {file_name}")
    
    return ipo_df_f

# ### 6. 중복청약확인 대상 IPO 캘린더 생성
def create_ipo_calendar(ipo_df_f):
    now = datetime.now()
    print(
        now.year
        , now.month
        , now.day
        , now.hour
        , now.minute
        , now.second
    ) 
    year = now.year


    #create workbook 
    wb = Workbook()

    for month in range(1,13) : 
        if month == 1 : 
            ws = wb.active 
            ws.title = "1월" 
        else : 
            ws = wb.create_sheet(str(month) + "월") 
        
        set_title(ws, str(month) + "월") 
        set_weeks_title(ws) 
        set_ipo_calendar(ws, year, month, ipo_df_f) 
        
    wb.save(filename="./output/IPO일정_" + str(year) +".xlsx")

