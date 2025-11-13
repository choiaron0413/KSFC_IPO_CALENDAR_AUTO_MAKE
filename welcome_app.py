# welcome_app.py

import streamlit as st
import datetime
from datetime import date
from ipo_search import (
    scrawl_ipo_schedule,
    filter_ipo_schedule,
    filter_ipo_by_inq_dt,
    save_ipo_schedule_to_excel,
    create_ipo_calendar
)

import time


def make_IPO_calendar(st_dt, nd_dt):
    inq_st_dt = st_dt
    inq_nd_dt = nd_dt
    # IPO 일정 스크래핑
    try:
        y = st.empty()
        with st.spinner("⏳ IPO 일정 스크래핑 중...(인내심 필요)"): 
            ipo_df_f = scrawl_ipo_schedule()
        st.success(f"✅  IPO 일정 스크래핑 완료. ")
    except Exception as e:
        st.error(f"❗ IPO 일정 스크래핑 중 오류가 발생했습니다: {e}")
        return False

    # 2개 이상 인수회사인 종목 필터링
    try:
        ipo_df_f = filter_ipo_schedule(ipo_df_f)
        st.success(f"✅ 2개 이상 인수회사인 종목 필터링 완료. ")
    except Exception as e:
        st.error(f"❗ 인수회사 2개 이상인 종목 필터링 중 오류가 발생했습니다: {e}")
        return False
    
    # 조회기간 필터 적용
    try:
        ipo_df_f = filter_ipo_by_inq_dt(ipo_df_f, inq_st_dt, inq_nd_dt)
        st.success(f"✅ 조회기간 필터 적용 완료. ")
    except Exception as e:
        st.error(f"❗ 조회기간 필터 적용 중 오류가 발생했습니다: {e}")
        return False
    
    # 중복청약확인 대상 종목정보 엑셀파일 
    try:
        ipo_df_f = save_ipo_schedule_to_excel(ipo_df_f, inq_st_dt, inq_nd_dt)
        st.success(f"✅ 중복청약확인 대상 종목정보 엑셀파일 저장 완료. ")
    except Exception as e:
        st.error(f"❗ 중복청약확인 대상 종목정보 엑셀파일 저장 중 오류가 발생했습니다: {e}")
        return False
    # 중복청약확인 대상 IPO 캘린더 생성
    try:
        create_ipo_calendar(ipo_df_f)
        st.success(f"✅ 중복청약확인 대상 IPO 캘린더 생성 완료. ")
    except Exception as e:
        st.error(f"❗ 중복청약확인 대상 IPO 캘린더 생성 중 오류가 발생했습니다: {e}")
        return False
    return True


# ----------------------------------------------------
# 1. 커스텀 CSS 삽입 (수정 완료)
# ----------------------------------------------------
# ----- 스타일 (다중 선택자, 우선순위 강제) -----
custom_css = """
<style>
/* fallback: 모든 Streamlit 버튼 스타일 (너무 넓으면 제거) */
div[data-testid^="stButton"] > button,
button[aria-label] {
    border-radius: 0.5rem !important;
    border: 1px solid #FF6262 !important;
}


/* 날짜 위젯 스타일 (원래 있던 것) */
.stDateInput {
    border-radius: 5px;
    padding: 5px;
    max-width: 150px;
}
</style>
"""

# HTML/CSS를 Streamlit 앱에 안전하게 삽입
st.markdown(custom_css, unsafe_allow_html=True)


st.title("📆 [KSFC 중복청약] IPO 캘린더 수기 생성 ✨")


st.markdown("---")

st.markdown("### ** 아직 완전한 자동화까진 못했어요😢 ")
st.markdown("##### ** 대신 :red[딸깍]으로 IPO캘린더를 만들 수 있어요! ")
st.markdown("##### ** :red[아래 조회일자를 입력 후] 생성버튼을 눌러주세요! ")
st.markdown("---")
today_date = date.today()
after_30_days = today_date + datetime.timedelta(days=30)

# 1. 조회 시작일자 (볼드 및 크기 설정)
st.markdown("### **📅 조회 시작일자**", unsafe_allow_html=True)
# 라벨을 숨기고 ('' 사용) 상단 마크다운으로 스타일링된 라벨을 대체합니다.
st_dt = st.date_input('', value=today_date, key='st_dt_input') 

# 2. 조회 종료일자 (볼드 및 크기 설정)
st.markdown("### **📅 조회 종료일자**", unsafe_allow_html=True)
nd_dt = st.date_input('', value=after_30_days, key='nd_dt_input')


# HTML/CSS를 Streamlit 앱에 안전하게 삽입
st.markdown(custom_css, unsafe_allow_html=True)

if st.button("🎁 대상 기간의 IPO 캘린더를 생성", key="btn_step1", use_container_width=False ):
    st.markdown("---")
    st.success(f"✅ {st_dt} 부터 {nd_dt} 까지의 IPO 캘린더를 생성합니다!")
    y = st.empty()
    with y:
        for i in range(4):
            t =  3-i
            y.empty()
            st.write(f"{t} 초 후 생성 시작...")
            time.sleep(1)
    result = make_IPO_calendar(st_dt, nd_dt)

    if(result != False):
        st.success("✅ IPO 캘린더 생성이 완료되었습니다! 'output' 폴더에서 파일을 확인하세요."  )
    else:
        st.error("❗ IPO 캘린더 생성에 실패했습니다. 오류 메시지를 확인해주세요.")

