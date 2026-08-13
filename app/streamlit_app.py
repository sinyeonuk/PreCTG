"""PreCTG polished-demonstration shell."""

from __future__ import annotations

import streamlit as st

from prectg.metadata import NON_CLINICAL_WARNING, project_status

st.set_page_config(page_title="PreCTG", page_icon="🫀", layout="wide")

st.markdown(
    """
    <style>
    :root, html, body, [class*="css"] {
        font-family: "Pretendard", "Apple SD Gothic Neo", "Noto Sans KR",
                     "Malgun Gothic", sans-serif;
    }
    .block-container { max-width: 1080px; padding-top: 2.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

status = project_status()
st.title("PreCTG")
st.caption("분만 전 EMR과 초기 CTG 정보를 단계적으로 연결하는 조기경보 MVP")
st.warning(NON_CLINICAL_WARNING)

left, right = st.columns(2)
with left:
    st.subheader("현재 준비된 항목")
    for item in status["implemented"]:
        st.write(f"- {item}")
with right:
    st.subheader("다음 구현 항목")
    for item in status["not_implemented"]:
        st.write(f"- {item}")

st.info("현재 화면은 프로젝트 골격 확인용입니다. 환자 입력이나 예측 기능은 아직 제공하지 않습니다.")
