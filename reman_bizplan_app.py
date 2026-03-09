"""
자동차 재제조 사업계획서 관리 앱
실행 방법: streamlit run reman_bizplan_app.py
"""

import streamlit as st
import json
import os
from datetime import datetime

# ─────────────────────────────────────────
# 설정
# ─────────────────────────────────────────
DATA_FILE = "bizplan_data.json"

st.set_page_config(
    page_title="ReMan BizPlan | 자동차 재제조 사업계획서",
    page_icon="🔩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CSS 스타일
# ─────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    .main { background-color: #0f1117; }
    .stApp { background-color: #0f1117; }

    /* 헤더 타이틀 */
    .app-header {
        background: linear-gradient(135deg, #1a1200, #2a2000);
        border: 1px solid #e8a020;
        border-radius: 12px;
        padding: 24px 32px;
        margin-bottom: 24px;
        text-align: center;
    }
    .app-header h1 { color: #f5c842; margin: 0; font-size: 26px; font-weight: 900; }
    .app-header p { color: #888; margin: 4px 0 0; font-size: 13px; }

    /* 카드 */
    .plan-card {
        background: #1a1d27;
        border: 1px solid #2a2d3e;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 12px;
        transition: border-color 0.2s;
    }
    .plan-card:hover { border-color: #e8a020; }
    .plan-card h3 { color: #f5c842; margin: 0 0 4px; font-size: 16px; }
    .plan-card p { color: #666; margin: 0; font-size: 12px; }

    /* 섹션 헤더 */
    .section-header {
        border-left: 4px solid #e8a020;
        padding-left: 12px;
        margin: 24px 0 16px;
        color: #f5c842;
        font-size: 16px;
        font-weight: 800;
    }

    /* 진행률 텍스트 */
    .progress-label {
        color: #f5c842;
        font-size: 13px;
        font-weight: 700;
        text-align: right;
    }

    /* 미리보기 */
    .preview-box {
        background: #1a1d27;
        border: 1px solid #2a2d3e;
        border-radius: 12px;
        padding: 32px 40px;
    }
    .preview-title {
        text-align: center;
        border-bottom: 3px solid #e8a020;
        padding-bottom: 20px;
        margin-bottom: 28px;
    }
    .preview-title h1 { color: #f5c842; font-size: 24px; margin: 4px 0; }
    .preview-title p { color: #888; margin: 0; font-size: 12px; }
    .field-row { display: flex; gap: 16px; margin-bottom: 10px; font-size: 13px; }
    .field-label { color: #888; min-width: 140px; flex-shrink: 0; }
    .field-value { color: #e8e8f0; line-height: 1.6; white-space: pre-wrap; }

    /* 사이드바 */
    section[data-testid="stSidebar"] {
        background-color: #14171f !important;
        border-right: 1px solid #2a2d3e;
    }
    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        text-align: left;
        background: transparent;
        border: 1px solid transparent;
        color: #888;
        font-size: 13px;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 2px;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        border-color: #e8a020;
        color: #f5c842;
        background: rgba(232,160,32,0.08);
    }

    /* 버튼 */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
        font-size: 13px;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        background-color: #1a1d27 !important;
        border: 1px solid #2a2d3e !important;
        color: #e8e8f0 !important;
        border-radius: 8px;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #e8a020 !important;
    }

    /* 성공/경고 메시지 */
    .stSuccess, .stInfo { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 데이터 구조
# ─────────────────────────────────────────
SECTIONS = [
    ("overview",   "🏭 사업 개요"),
    ("market",     "📊 시장 분석"),
    ("product",    "⚙️ 제품/서비스"),
    ("operation",  "🔧 운영 계획"),
    ("finance",    "💰 재무 계획"),
    ("risk",       "⚠️ 리스크 관리"),
]

FIELD_LABELS = {
    "overview": {
        "companyName": "회사명",
        "ceo": "대표자명",
        "founded": "설립일",
        "address": "소재지",
        "bizType": "업종",
        "capital": "자본금(원)",
        "employees": "임직원 수",
        "vision": "비전",
        "mission": "미션",
        "summary": "사업 요약",
    },
    "market": {
        "targetMarket": "목표 시장",
        "marketSize": "시장 규모",
        "competitors": "경쟁사 현황",
        "advantage": "경쟁 우위",
        "trend": "시장 트렌드",
        "strategy": "시장 진입 전략",
    },
    "product": {
        "mainProducts": "주요 재제조 품목",
        "remanProcess": "재제조 공정 개요",
        "quality": "품질 관리 방안",
        "certification": "보유/취득 예정 인증",
        "procurement": "부품 조달 계획",
        "technology": "핵심 기술 및 노하우",
    },
    "operation": {
        "facility": "생산 시설 현황",
        "equipment": "주요 설비 목록",
        "workforce": "인력 구성 계획",
        "process": "생산 프로세스",
        "partner": "협력사 현황",
        "logistics": "물류/배송 계획",
    },
    "finance": {
        "investment": "초기 투자 비용(원)",
        "revenue1": "1년차 예상 매출(원)",
        "revenue2": "2년차 예상 매출(원)",
        "revenue3": "3년차 예상 매출(원)",
        "cost": "주요 원가 구조",
        "profit": "예상 영업이익률(%)",
        "funding": "자금 조달 계획",
        "breakeven": "손익분기점 분석",
    },
    "risk": {
        "supplyRisk": "부품 공급망 리스크",
        "qualityRisk": "품질/불량 리스크",
        "marketRisk": "시장/수요 리스크",
        "regulatoryRisk": "규제/인증 리스크",
        "mitigationPlan": "리스크 대응 전략",
    },
}

LARGE_FIELDS = {
    "summary", "vision", "mission", "strategy", "advantage", "trend",
    "remanProcess", "quality", "technology", "process", "partner",
    "cost", "funding", "breakeven", "mitigationPlan", "procurement",
    "logistics", "workforce", "competitors",
}

EMPTY_PLAN = {sec: {f: ("자동차 부품 재제조업" if f == "bizType" else "") for f in FIELD_LABELS[sec]} for sec, _ in SECTIONS}


# ─────────────────────────────────────────
# 파일 저장/불러오기
# ─────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(plans):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(plans, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────
# Session State 초기화
# ─────────────────────────────────────────
if "plans" not in st.session_state:
    st.session_state.plans = load_data()
if "view" not in st.session_state:
    st.session_state.view = "list"       # list | edit | preview
if "current_id" not in st.session_state:
    st.session_state.current_id = None
if "form_data" not in st.session_state:
    st.session_state.form_data = {s: dict(v) for s, v in EMPTY_PLAN.items()}
if "active_section" not in st.session_state:
    st.session_state.active_section = "overview"


# ─────────────────────────────────────────
# 완성도 계산
# ─────────────────────────────────────────
def completion_rate(data):
    total = filled = 0
    for sec in data.values():
        for v in sec.values():
            total += 1
            if str(v).strip():
                filled += 1
    return int(filled / total * 100) if total else 0


# ─────────────────────────────────────────
# 헤더
# ─────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <h1>🔩 ReMan BizPlan</h1>
  <p>자동차 재제조 사업계획서 작성 & 관리 시스템</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# 사이드바 – 네비게이션
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📋 메뉴")

    if st.button("🏠  사업계획서 목록", key="nav_list"):
        st.session_state.view = "list"
        st.rerun()

    if st.button("➕  새 사업계획서 작성", key="nav_new"):
        st.session_state.form_data = {s: dict(v) for s, v in EMPTY_PLAN.items()}
        st.session_state.current_id = None
        st.session_state.active_section = "overview"
        st.session_state.view = "edit"
        st.rerun()

    if st.session_state.view == "edit":
        st.markdown("---")
        st.markdown("### 📑 섹션 이동")
        rate = completion_rate(st.session_state.form_data)
        st.progress(rate / 100)
        st.markdown(f'<div class="progress-label">✅ {rate}% 완성</div>', unsafe_allow_html=True)
        st.markdown("")
        for sec_id, sec_label in SECTIONS:
            if st.button(sec_label, key=f"nav_{sec_id}"):
                st.session_state.active_section = sec_id
                st.rerun()

    st.markdown("---")
    st.markdown('<div style="color:#444;font-size:11px;text-align:center;">ReMan BizPlan v1.0<br>자동차 재제조 전문 관리</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────
# 목록 화면
# ─────────────────────────────────────────
if st.session_state.view == "list":
    plans = st.session_state.plans

    if not plans:
        st.info("📋 아직 작성된 사업계획서가 없습니다. 사이드바에서 '새 사업계획서 작성'을 클릭하세요.")
    else:
        st.markdown(f"**총 {len(plans)}개의 사업계획서**")
        for plan in plans:
            with st.container():
                col1, col2, col3 = st.columns([6, 1, 1])
                with col1:
                    rate = completion_rate(plan["data"])
                    st.markdown(f"""
                    <div class="plan-card">
                        <h3>🏭 {plan['name']}</h3>
                        <p>생성: {plan['createdAt']} &nbsp;·&nbsp; 수정: {plan['updatedAt']} &nbsp;·&nbsp; 완성도: {rate}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("✏️ 편집", key=f"edit_{plan['id']}"):
                        st.session_state.form_data = {s: dict(plan["data"].get(s, {})) for s, _ in SECTIONS}
                        st.session_state.current_id = plan["id"]
                        st.session_state.active_section = "overview"
                        st.session_state.view = "edit"
                        st.rerun()
                with col3:
                    if st.button("📄 보기", key=f"view_{plan['id']}"):
                        st.session_state.form_data = {s: dict(plan["data"].get(s, {})) for s, _ in SECTIONS}
                        st.session_state.current_id = plan["id"]
                        st.session_state.view = "preview"
                        st.rerun()


# ─────────────────────────────────────────
# 편집 화면
# ─────────────────────────────────────────
elif st.session_state.view == "edit":
    sec_id = st.session_state.active_section
    sec_label = dict(SECTIONS)[sec_id]
    fields = FIELD_LABELS[sec_id]
    data = st.session_state.form_data

    st.markdown(f'<div class="section-header">{sec_label}</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#666;font-size:12px;margin-bottom:20px;">각 항목을 입력하세요. 입력 후 저장 버튼을 누르세요.</div>', unsafe_allow_html=True)

    updated = {}
    for field, label in fields.items():
        current_val = data[sec_id].get(field, "")
        if field in LARGE_FIELDS:
            val = st.text_area(label, value=current_val, height=100, key=f"field_{sec_id}_{field}")
        else:
            val = st.text_input(label, value=current_val, key=f"field_{sec_id}_{field}")
        updated[field] = val

    # 폼 데이터 업데이트
    st.session_state.form_data[sec_id] = updated

    st.markdown("---")
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

    sec_ids = [s for s, _ in SECTIONS]
    cur_idx = sec_ids.index(sec_id)

    with col1:
        if cur_idx > 0:
            if st.button("← 이전 섹션"):
                st.session_state.active_section = sec_ids[cur_idx - 1]
                st.rerun()

    with col2:
        if cur_idx < len(sec_ids) - 1:
            if st.button("다음 섹션 →"):
                st.session_state.active_section = sec_ids[cur_idx + 1]
                st.rerun()

    with col3:
        if st.button("💾 저장", type="primary"):
            name = st.session_state.form_data["overview"].get("companyName") or "미입력 사업계획서"
            now = datetime.now().strftime("%Y-%m-%d")
            plans = st.session_state.plans
            if st.session_state.current_id:
                for p in plans:
                    if p["id"] == st.session_state.current_id:
                        p["name"] = name
                        p["updatedAt"] = now
                        p["data"] = {s: dict(v) for s, v in st.session_state.form_data.items()}
                        break
            else:
                new_id = int(datetime.now().timestamp() * 1000)
                plans.append({"id": new_id, "name": name, "createdAt": now, "updatedAt": now,
                               "data": {s: dict(v) for s, v in st.session_state.form_data.items()}})
                st.session_state.current_id = new_id
            st.session_state.plans = plans
            save_data(plans)
            st.success("✅ 저장되었습니다!")

    with col4:
        if st.button("📄 미리보기"):
            st.session_state.view = "preview"
            st.rerun()


# ─────────────────────────────────────────
# 미리보기 화면
# ─────────────────────────────────────────
elif st.session_state.view == "preview":
    data = st.session_state.form_data
    company = data["overview"].get("companyName") or "회사명 미입력"
    ceo = data["overview"].get("ceo", "")
    now_str = datetime.now().strftime("%Y년 %m월 %d일")

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("✏️ 편집으로 돌아가기"):
            st.session_state.view = "edit"
            st.rerun()
    with col_btn2:
        if st.button("🏠 목록으로"):
            st.session_state.view = "list"
            st.rerun()

    st.markdown("---")

    # 표지
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1200,#2a2000);border:2px solid #e8a020;
                border-radius:16px;padding:40px;text-align:center;margin-bottom:28px;">
        <div style="font-size:12px;color:#e8a020;letter-spacing:0.2em;margin-bottom:8px;">BUSINESS PLAN</div>
        <h1 style="color:#f5c842;font-size:28px;margin:0 0 8px;font-weight:900;">{company}</h1>
        <div style="color:#888;font-size:13px;">자동차 부품 재제조 사업계획서</div>
        {"<div style='color:#ccc;font-size:13px;margin-top:8px;'>대표자: " + ceo + "</div>" if ceo else ""}
        <div style="color:#555;font-size:11px;margin-top:12px;">{now_str} 기준</div>
    </div>
    """, unsafe_allow_html=True)

    # 각 섹션 출력
    for sec_id, sec_label in SECTIONS:
        sec_data = data.get(sec_id, {})
        fields = FIELD_LABELS[sec_id]
        has_content = any(str(v).strip() for v in sec_data.values())
        if not has_content:
            continue

        st.markdown(f'<div class="section-header">{sec_label}</div>', unsafe_allow_html=True)
        rows_html = ""
        for field, label in fields.items():
            val = sec_data.get(field, "")
            if not str(val).strip():
                continue
            rows_html += f'<div class="field-row"><span class="field-label">{label}</span><span class="field-value">{val}</span></div>'

        st.markdown(f'<div style="padding-left:16px;">{rows_html}</div>', unsafe_allow_html=True)
        st.markdown("")

    st.markdown("---")
    st.markdown(f'<div style="text-align:center;color:#444;font-size:11px;">ReMan BizPlan · 자동차 재제조 사업계획서 관리 시스템</div>', unsafe_allow_html=True)
