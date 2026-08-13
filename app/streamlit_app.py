"""Polished, offline-capable Streamlit demonstration for PreCTG."""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from prectg.codebook import code_to_label
from prectg.explanation import signal_label
from prectg.features import training_feature_frame
from prectg.metadata import NON_CLINICAL_WARNING
from prectg.model import train_model_bundle
from prectg.risk_engine import analyze_payload
from prectg.schema import AnalysisResult
from prectg.synthetic import generate_synthetic_data

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "data" / "fixtures" / "minimal-synthetic-input.json"
FONT_PATH = ROOT / "app" / "assets" / "fonts" / "Pretendard-Regular.woff2"
CASE_LABELS = {
    "normal": ("기본 사례", "추가 합성 패턴이 적은 입력"),
    "maternal": ("분만 전 관찰 사례", "분만 전 정보에 합성 패턴이 있는 입력"),
    "ctg": ("초기 CTG 관찰 사례", "초기 CTG에 합성 패턴이 있는 입력"),
    "combined": ("복합 관찰 사례", "두 단계에 합성 패턴이 함께 있는 입력"),
    "missing": ("결측 사례", "일부 입력이 없어 단계 결과가 제한되는 입력"),
    "conflict": ("규칙 충돌 사례", "서로 다른 CTG 패턴이 함께 있는 입력"),
}
STATUS_LABELS = {
    "available": "분석 완료",
    "insufficient_data": "입력 부족",
    "unavailable": "결과 없음",
    "not_applicable": "분석 대상 아님",
    "failed": "분석 실패",
}

st.set_page_config(page_title="PreCTG", page_icon="♥", layout="wide")


def _font_css() -> str:
    if not FONT_PATH.exists():
        return ""
    encoded = base64.b64encode(FONT_PATH.read_bytes()).decode("ascii")
    return (
        "@font-face{font-family:'Pretendard';font-style:normal;font-weight:100 900;"
        f"font-display:swap;src:url(data:font/woff2;base64,{encoded}) format('woff2');}}"
    )


st.markdown(
    f"""
    <style>
    {_font_css()}
    :root {{ --ink:#162323; --muted:#5e6d6b; --line:#dce5e2; --soft:#f3f7f5;
            --brand:#126c61; --brand-dark:#0d5149; --high:#a63d40; --review:#996515; }}
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
      font-family:"Pretendard","Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",sans-serif;
      color:var(--ink);
    }}
    [data-testid="stAppViewContainer"] {{ background:#f8faf9; }}
    .block-container {{ max-width:1080px; padding:4.5rem 2rem 4rem; }}
    h1 {{ letter-spacing:-.04em!important; font-size:2.15rem!important;
          margin-bottom:.25rem!important; }}
    h2, h3 {{ letter-spacing:-.025em!important; }}
    .eyebrow {{ color:var(--brand); font-size:.78rem; font-weight:800; letter-spacing:.08em; }}
    .lead {{ color:var(--muted); font-size:1.02rem; margin:.25rem 0 1.2rem; }}
    .notice {{ border:1px solid #d8e4df; background:#eef5f2; padding:.85rem 1rem;
               border-radius:10px; color:#334e49; font-size:.9rem; }}
    .steps {{ display:grid; grid-template-columns:repeat(3,1fr); gap:.5rem; margin:1.5rem 0 2rem; }}
    .step {{ border-top:3px solid var(--line); padding:.65rem .2rem;
             color:var(--muted); font-size:.88rem; }}
    .step.active {{ border-color:var(--brand); color:var(--brand-dark); font-weight:800; }}
    .step.done {{ border-color:#79a99f; color:#385f58; }}
    .result-banner {{ padding:1.1rem 1.2rem; border-radius:12px; border-left:5px solid var(--brand);
                      background:white; box-shadow:0 6px 24px rgba(23,54,49,.07);
                      margin-bottom:1rem; }}
    .signal-high {{ border-left-color:var(--high); }}
    .signal-review {{ border-left-color:var(--review); }}
    .result-kicker {{ color:var(--muted); font-size:.82rem; }}
    .result-title {{ font-size:1.55rem; font-weight:850; margin-top:.15rem; }}
    [data-testid="stForm"], [data-testid="stVerticalBlockBorderWrapper"] {{
      background:white; border-color:var(--line)!important; border-radius:12px!important;
    }}
    .stButton button, .stDownloadButton button {{ min-height:44px; border-radius:8px;
                                                   font-weight:750; }}
    .stButton button[kind="primary"] {{ background:var(--brand); border-color:var(--brand); }}
    .stButton button[kind="primary"]:hover {{ background:var(--brand-dark);
                                                border-color:var(--brand-dark); }}
    *:focus-visible {{ outline:3px solid #50a99a!important; outline-offset:2px!important; }}
    @media (max-width:640px) {{
      .block-container {{ padding:4rem 1rem 3rem; }}
      .steps {{ gap:.3rem; }} .step {{ font-size:.75rem; }} h1 {{ font-size:1.8rem!important; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def representative_cases() -> dict[str, dict[str, Any]]:
    frame = generate_synthetic_data(rows=3000, seed=20260814, profile="distribution")
    probabilities = demo_model()["model"].predict_proba(training_feature_frame(frame))[:, 1]
    frame = frame.assign(_demo_probability=probabilities)
    cases: dict[str, dict[str, Any]] = {}
    for scenario in CASE_LABELS:
        candidates = frame.loc[frame["scenario_type"] == scenario]
        row = candidates.sort_values("_demo_probability").iloc[0 if scenario == "normal" else -1]
        cases[scenario] = {
            key: value
            for key, value in row.drop(labels="_demo_probability").to_dict().items()
            if not pd.isna(value)
        }
    return cases


@st.cache_resource(show_spinner=False)
def demo_model() -> dict[str, Any]:
    frame = generate_synthetic_data(rows=3000, seed=20260814, profile="distribution")
    bundle, _ = train_model_bundle(frame, seed=20260814)
    return bundle


def progress(step: int) -> None:
    labels = ("1. 사례 선택", "2. 입력 확인", "3. 분석 결과")
    items = []
    for index, label in enumerate(labels, start=1):
        state = "active" if index == step else "done" if index < step else ""
        items.append(f'<div class="step {state}">{label}</div>')
    st.markdown(f'<div class="steps">{"".join(items)}</div>', unsafe_allow_html=True)


def reset() -> None:
    for key in ("step", "payload", "result", "source_mode", "model_enabled"):
        st.session_state.pop(key, None)
    st.session_state.step = 1


def step_one() -> None:
    st.subheader("어떤 방식으로 시작할까요?")
    method = st.radio(
        "입력 방식",
        ["대표 사례", "직접 입력", "JSON 업로드"],
        horizontal=True,
        label_visibility="collapsed",
    )
    payload: dict[str, Any] | None = None
    if method == "대표 사례":
        cases = representative_cases()
        selected = st.selectbox(
            "대표 사례",
            list(CASE_LABELS),
            format_func=lambda value: f"{CASE_LABELS[value][0]} — {CASE_LABELS[value][1]}",
        )
        payload = cases[selected]
        st.info("모든 수치와 결과는 기능 확인을 위해 생성한 합성 사례입니다.")
    elif method == "직접 입력":
        payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        st.info("기본 입력을 다음 단계에서 직접 수정합니다.")
    else:
        st.warning("실제 환자정보나 식별정보가 포함된 파일은 업로드하지 마세요.")
        uploaded = st.file_uploader("AIHub 호환 JSON 파일", type=["json"])
        if uploaded:
            try:
                loaded = json.load(uploaded)
                if not isinstance(loaded, dict):
                    raise ValueError
                payload = loaded
                st.success("JSON을 읽었습니다. 다음 단계에서 입력값을 확인해 주세요.")
            except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
                st.error(
                    f"{uploaded.name}의 JSON 구조를 확인해 주세요. 최상위 값은 객체여야 합니다."
                )

    model_enabled = st.checkbox(
        "ML 분석 포함",
        value=True,
        help="끄면 규칙 결과만 유지되고 ML 단계는 모델 결과 없음으로 표시됩니다.",
    )
    if not model_enabled:
        st.caption("규칙 기반 결과만 표시합니다. 사용할 수 있는 ML 모델이 없습니다.")

    left, right = st.columns([3, 1])
    with left:
        if st.button("입력 초기화", use_container_width=True):
            reset()
            st.rerun()
    with right:
        if st.button(
            "입력 확인", type="primary", disabled=payload is None, use_container_width=True
        ):
            st.session_state.payload = payload
            st.session_state.source_mode = method
            st.session_state.model_enabled = model_enabled
            st.session_state.step = 2
            st.rerun()


def _number(payload: dict[str, Any], key: str, default: int) -> int:
    value = payload.get(key, default)
    return default if value is None or pd.isna(value) else int(value)


def _choice(value: Any, choices: list[str], default: str) -> int:
    normalized = str(value if value is not None else default)
    return choices.index(normalized) if normalized in choices else choices.index(default)


def _code_select(label: str, field: str, choices: list[str], value: Any, default: str) -> str:
    return st.selectbox(
        label,
        choices,
        index=_choice(value, choices, default),
        format_func=lambda code: code_to_label(field, code),
    )


def step_two() -> None:
    st.subheader("분석에 사용할 입력을 확인해 주세요")
    model_scope = "규칙과 ML 분석" if st.session_state.get("model_enabled", True) else "규칙 분석만"
    st.caption(f"입력 출처: {st.session_state.get('source_mode', '대표 사례')} · {model_scope}")
    with st.expander("분석에 사용하는 정보"):
        st.write(
            "모델 입력: 임신·출산 횟수, 임신 주수, 기저 심박수와 초기 CTG 코드. "
            "식별자, 정답, 출생 이후 결과와 합성 생성 메타데이터는 모델에서 제외합니다."
        )
    payload = dict(st.session_state.payload)
    with st.form("input-review", border=True):
        left, right = st.columns(2)
        with left:
            st.markdown("#### 분만 전 정보")
            record_id = st.text_input("사례 식별자", value=str(payload.get("ID", "")))
            gravida = st.number_input("임신 횟수", 0, 20, _number(payload, "Mother.Gravida", 1))
            para = st.number_input("출산 횟수", 0, 20, _number(payload, "Mother.Para", 0))
            ga_missing = st.checkbox("임신 주수 값 없음", value="GA.wks" not in payload)
            ga_weeks = st.number_input(
                "임신 주수(주)", 0, 50, _number(payload, "GA.wks", 39), disabled=ga_missing
            )
            ga_days = st.number_input("추가 일수", 0, 6, _number(payload, "GA.day", 0))
        with right:
            st.markdown("#### 초기 CTG 정보")
            baseline_missing = st.checkbox("기저 심박수 값 없음", value="BaseLine" not in payload)
            baseline = st.number_input(
                "기저 심박수(bpm)",
                0,
                250,
                _number(payload, "BaseLine", 140),
                disabled=baseline_missing,
            )
            variability = _code_select(
                "기저 변이도 코드",
                "Baseline_Variability",
                ["0", "1", "2", "3"],
                payload.get("Baseline_Variability"),
                "2",
            )
            acceleration = _code_select(
                "가속 코드", "Acceleration", ["1", "2"], payload.get("Acceleration"), "1"
            )
            late = _code_select(
                "후기 감속 코드",
                "Late_deceleration",
                ["0", "1", "2"],
                payload.get("Late_deceleration"),
                "0",
            )
            variable = _code_select(
                "가변 감속 코드",
                "Variable_deceleration",
                ["0", "1", "2"],
                payload.get("Variable_deceleration"),
                "0",
            )
            prolonged = _code_select(
                "지연 감속 코드",
                "Prolonged_deceleration",
                ["0", "1"],
                payload.get("Prolonged_deceleration"),
                "0",
            )
            sinusoidal = _code_select(
                "사인파형 코드",
                "Sinosoical_pattern",
                ["0", "1"],
                payload.get("Sinosoical_pattern"),
                "0",
            )
        back_col, submit_col = st.columns([3, 1])
        with back_col:
            back = st.form_submit_button("이전", use_container_width=True)
        with submit_col:
            submitted = st.form_submit_button("분석 실행", type="primary", use_container_width=True)
    if back:
        st.session_state.step = 1
        st.rerun()
    if submitted:
        payload.update(
            {
                "ID": record_id,
                "Mother.Gravida": gravida,
                "Mother.Para": para,
                "GA.wks": None if ga_missing else ga_weeks,
                "GA.day": ga_days,
                "BaseLine": None if baseline_missing else baseline,
                "Baseline_Variability": variability,
                "Acceleration": acceleration,
                "Late_deceleration": late,
                "Variable_deceleration": variable,
                "Prolonged_deceleration": prolonged,
                "Sinosoical_pattern": sinusoidal,
            }
        )
        with st.spinner("입력값을 확인하고 단계별 위험 신호를 분석하고 있습니다."):
            bundle = demo_model() if st.session_state.get("model_enabled", True) else None
            result = analyze_payload(payload, bundle)
        if result.validation.status == "invalid":
            for issue in result.validation.errors:
                st.error(f"{issue.message} {issue.action or ''}")
            st.session_state.payload = payload
        else:
            st.session_state.payload = payload
            st.session_state.result = result.model_dump(mode="json")
            st.session_state.step = 3
            st.rerun()


def step_three() -> None:
    result = AnalysisResult.model_validate(st.session_state.result)
    signal = result.integrated_result.signal
    st.markdown(
        f'<div class="result-banner signal-{signal.value}">'
        '<div class="result-kicker">통합 시연 결과</div>'
        f'<div class="result-title">{signal_label(signal)}</div></div>',
        unsafe_allow_html=True,
    )
    first, second, third = st.columns(3)
    first.metric("사용한 단계", f"{len(result.integrated_result.used_stages)} / 3")
    second.metric("입력 완전성", f"{result.completeness.overall_ratio * 100:.0f}%")
    probability = result.stages["stage_2"].probability
    third.metric(
        "합성 모델 확률", "결과 없음" if probability is None else f"{probability * 100:.1f}%"
    )

    st.subheader("단계별 판단 근거")
    labels = {
        "stage_0": "0단계 · 분만 전 정보",
        "stage_1": "1단계 · 초기 CTG",
        "stage_2": "2단계 · ML 분석",
    }
    columns = st.columns(3)
    for column, (key, label) in zip(columns, labels.items(), strict=True):
        stage = result.stages[key]
        with column, st.container(border=True):
            st.markdown(f"**{label}**")
            st.markdown(f"### {signal_label(stage.signal)}")
            st.caption(f"상태: {STATUS_LABELS[stage.status.value]}")
            for reason in stage.reasons[:3]:
                st.write(f"- {reason.title}: {reason.detail}")
    if result.completeness.missing_fields:
        with st.expander("누락된 입력 확인"):
            st.write(", ".join(result.completeness.missing_fields))
    with st.expander("분석 계약 정보"):
        st.write(
            f"입력 {result.contract.input_version} · 관찰창 {result.contract.window_version} · "
            f"목표 {result.contract.target_version} · 결과 {result.contract.result_version}"
        )
    st.warning(NON_CLINICAL_WARNING)
    serialized = json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2)
    back_col, reset_col, download_col = st.columns([2, 2, 1.4])
    with back_col:
        if st.button("입력 수정", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    with reset_col:
        if st.button("새 사례 분석", use_container_width=True):
            reset()
            st.rerun()
    with download_col:
        st.download_button(
            "결과 JSON 저장",
            serialized,
            file_name="prectg-demo-result.json",
            mime="application/json",
            type="primary",
            use_container_width=True,
        )


if "step" not in st.session_state:
    st.session_state.step = 1

st.markdown('<div class="eyebrow">DEBUGLAB · SYNTHETIC DEMO</div>', unsafe_allow_html=True)
st.title("PreCTG")
st.markdown(
    '<div class="lead">분만 전 정보와 초기 CTG를 단계적으로 연결해 '
    "위험 신호의 변화를 살펴봅니다.</div>",
    unsafe_allow_html=True,
)
st.markdown(f'<div class="notice">{NON_CLINICAL_WARNING}</div>', unsafe_allow_html=True)
progress(st.session_state.step)

if st.session_state.step == 1:
    step_one()
elif st.session_state.step == 2:
    step_two()
else:
    step_three()
