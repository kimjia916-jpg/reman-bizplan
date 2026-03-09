"""
자동차 부품 순환경제 혁신 인프라 구축 사업 관리 앱
광주미래차모빌리티진흥원
실행: streamlit run reman_bizplan_app.py
"""

import streamlit as st
import json, os
from datetime import datetime, date

DATA_FILE  = "app_data.json"
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(
    page_title="자동차 부품 순환경제 사업관리",
    page_icon="🔩", layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;900&display=swap');
html,body,[class*="css"]{font-family:'Noto Sans KR',sans-serif;}
.stApp{background:#f4f6fb;}
.main-header{background:linear-gradient(135deg,#1e3a5f,#2563eb);border-radius:14px;
  padding:20px 32px;margin-bottom:20px;text-align:center;box-shadow:0 4px 20px rgba(37,99,235,0.18);}
.main-header h1{color:#fff;margin:0;font-size:20px;font-weight:900;}
.main-header p{color:rgba(255,255,255,0.75);margin:4px 0 0;font-size:12px;}
.sec-title{border-left:4px solid #2563eb;padding-left:12px;color:#1e3a5f;
  font-size:15px;font-weight:800;margin:0 0 14px;}
.file-row{display:flex;align-items:center;gap:12px;padding:10px 14px;
  background:#fff;border:1px solid #e2e8f0;border-radius:10px;margin-bottom:8px;}
.file-name{font-weight:600;font-size:13px;color:#1e293b;}
.file-meta{font-size:11px;color:#94a3b8;margin-top:2px;}
.tag{display:inline-block;padding:2px 8px;border-radius:20px;font-size:11px;font-weight:600;margin-right:4px;}
.tag-blue{background:#dbeafe;color:#1d4ed8;}
.tag-green{background:#dcfce7;color:#15803d;}
.tag-orange{background:#ffedd5;color:#c2410c;}
.tag-gray{background:#f1f5f9;color:#64748b;}
.sched-row{display:flex;gap:10px;align-items:flex-start;padding:12px 16px;
  background:#fff;border:1px solid #e2e8f0;border-radius:10px;margin-bottom:8px;}
.sched-date{font-size:11px;font-weight:700;color:#2563eb;min-width:80px;padding-top:2px;}
.sched-title{font-size:13px;font-weight:700;color:#1e293b;}
.sched-desc{font-size:12px;color:#64748b;margin-top:2px;}
.badge-d{padding:2px 10px;border-radius:20px;font-size:11px;font-weight:700;}
.d-urgent{background:#fee2e2;color:#dc2626;}
.d-soon{background:#fef3c7;color:#d97706;}
.d-ok{background:#dcfce7;color:#16a34a;}
.d-done{background:#f1f5f9;color:#94a3b8;}
section[data-testid="stSidebar"]{background:#fff!important;border-right:1px solid #e2e8f0;}
div[data-testid="stTextInput"] input,div[data-testid="stTextArea"] textarea{
  background:#fff!important;border:1px solid #e2e8f0!important;color:#1e293b!important;border-radius:8px;}
</style>
""", unsafe_allow_html=True)

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    return {"files":[],"schedules":[]}

def save(data):
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

if "data" not in st.session_state: st.session_state.data = load()
if "page" not in st.session_state: st.session_state.page = "dashboard"
data = st.session_state.data

st.markdown("""<div class="main-header">
  <h1>🔩 자동차 부품 순환경제 혁신 인프라 구축사업</h1>
  <p>광주미래차모빌리티진흥원 · 사업관리 시스템 · 2026~2030</p>
</div>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🗂️ 메뉴")
    for key, label in [("dashboard","🏠 대시보드"),("files","📁 자료 관리"),("schedule","📅 일정 관리")]:
        if st.button(label, key=f"m_{key}", use_container_width=True,
                     type="primary" if st.session_state.page==key else "secondary"):
            st.session_state.page=key; st.rerun()
    st.markdown("---")
    st.markdown('<div style="color:#94a3b8;font-size:11px;text-align:center;">ReMan BizPlan v2.0<br>광주미래차모빌리티진흥원</div>',unsafe_allow_html=True)

today = date.today()

# ══════════════════ 대시보드 ══════════════════
if st.session_state.page == "dashboard":
    st.markdown('<div class="sec-title">📊 사업 현황 요약</div>',unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    upcoming = sum(1 for s in data["schedules"] if s.get("date") and not s.get("done")
                   and 0 <= (date.fromisoformat(s["date"])-today).days <= 7)
    overdue  = sum(1 for s in data["schedules"] if s.get("date") and not s.get("done")
                   and date.fromisoformat(s["date"]) < today)
    with c1: st.metric("📁 등록 자료", f"{len(data['files'])}건")
    with c2: st.metric("📅 전체 일정", f"{len(data['schedules'])}건")
    with c3: st.metric("⚡ 7일 내 일정", f"{upcoming}건")
    with c4: st.metric("🔴 기한 초과", f"{overdue}건")
    st.markdown("---")

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="sec-title">📁 최근 등록 자료</div>',unsafe_allow_html=True)
        recent = sorted(data["files"],key=lambda x:x.get("uploaded_at",""),reverse=True)[:5]
        if not recent: st.info("등록된 자료가 없습니다.")
        for f in recent:
            ext = f["name"].split(".")[-1].upper() if "." in f["name"] else "FILE"
            tc = "tag-blue" if ext=="PDF" else "tag-green" if ext in ["XLSX","XLS"] else "tag-orange" if ext in ["DOCX","DOC","HWP"] else "tag-gray"
            st.markdown(f"""<div class="file-row"><div style="font-size:20px;">📄</div><div>
              <div class="file-name">{f['name']}</div>
              <div class="file-meta"><span class="tag {tc}">{ext}</span>{f.get('category','기타')} · {f.get('uploaded_at','')[:10]}</div>
            </div></div>""",unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="sec-title">📅 다가오는 일정</div>',unsafe_allow_html=True)
        ups = sorted([s for s in data["schedules"] if s.get("date") and not s.get("done")],key=lambda x:x["date"])[:6]
        if not ups: st.info("등록된 일정이 없습니다.")
        for s in ups:
            d = date.fromisoformat(s["date"])
            diff = (d-today).days
            if diff<0: badge=f'<span class="badge-d d-urgent">D+{abs(diff)} 초과</span>'
            elif diff==0: badge='<span class="badge-d d-urgent">D-Day</span>'
            elif diff<=7: badge=f'<span class="badge-d d-soon">D-{diff}</span>'
            else: badge=f'<span class="badge-d d-ok">D-{diff}</span>'
            st.markdown(f"""<div class="sched-row">
              <div class="sched-date">{s['date']}</div>
              <div><div class="sched-title">{s['title']} {badge}</div>
              <div class="sched-desc">{s.get('description','')[:60]}</div></div>
            </div>""",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="sec-title">📌 사업 기본 정보</div>',unsafe_allow_html=True)
    i1,i2 = st.columns(2)
    def info_row(k,v):
        return f'<div style="display:flex;gap:8px;padding:6px 0;border-bottom:1px solid #f1f5f9;font-size:13px;"><span style="color:#94a3b8;min-width:90px;">{k}</span><span style="color:#1e293b;font-weight:600;">{v}</span></div>'
    with i1:
        for k,v in [("사업명","자동차 부품 순환경제 혁신 인프라 구축 사업"),("사업기간","2026~2030년 (5년간)"),("주관기관","광주미래차모빌리티진흥원"),("참여기관","한국생산기술연구원 광주본부, 한국기초과학지원연구원"),("전문기관","KIAT")]:
            st.markdown(info_row(k,v),unsafe_allow_html=True)
    with i2:
        for k,v in [("총사업비","450억원"),("국비","99억원 (22%)"),("시비","80억원 (17.8%)"),("민자","271억원 (60.2%)"),("사업위치","광주 남구 에너지밸리산단")]:
            st.markdown(info_row(k,v),unsafe_allow_html=True)

# ══════════════════ 자료 관리 ══════════════════
elif st.session_state.page == "files":
    st.markdown('<div class="sec-title">📁 자료 관리</div>',unsafe_allow_html=True)

    with st.expander("➕ 새 자료 등록", expanded=True):
        st.markdown("""
        <style>
        [data-testid="stFileUploader"] {
            background: #f0f6ff;
            border: 2.5px dashed #2563eb;
            border-radius: 14px;
            padding: 10px 16px;
        }
        [data-testid="stFileUploader"]:hover {
            background: #dbeafe;
            border-color: #1d4ed8;
        }
        [data-testid="stFileUploaderDropzone"] {
            background: transparent !important;
        }
        [data-testid="stFileUploaderDropzoneInstructions"] {
            color: #2563eb !important;
            font-weight: 700 !important;
            font-size: 14px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "📂 파일을 여기에 드래그하거나 클릭해서 선택하세요",
            accept_multiple_files=True,
            type=["pdf","hwp","docx","doc","xlsx","xls","pptx","ppt","png","jpg","jpeg","txt","csv"],
            help="PDF, HWP, DOCX, XLSX, PPT, 이미지 등 여러 파일을 한번에 업로드할 수 있어요"
        )

        u1, u2 = st.columns(2)
        with u1:
            category = st.selectbox("분류",["공모/공고","협약서","사업계획서","예산/정산",
                "장비 관련","기업지원","SPC 설립","회의자료","보고서","인력양성","기타"])
        with u2:
            memo = st.text_input("메모 (선택)")

        if st.button("📤 업로드", type="primary") and uploaded:
            for f in uploaded:
                sp = os.path.join(UPLOAD_DIR, f.name)
                with open(sp,"wb") as out: out.write(f.getbuffer())
                data["files"].append({"id":int(datetime.now().timestamp()*1000),
                    "name":f.name,"size":f.size,"category":category,
                    "memo":memo,"path":sp,"uploaded_at":datetime.now().isoformat()})
            save(data)
            st.success(f"✅ {len(uploaded)}개 파일 등록 완료!")
            st.rerun()

    st.markdown("---")
    f1,f2 = st.columns(2)
    with f1: fc = st.selectbox("분류 필터",["전체","공모/공고","협약서","사업계획서","예산/정산","장비 관련","기업지원","SPC 설립","회의자료","보고서","인력양성","기타"])
    with f2: fk = st.text_input("🔍 파일명 검색")

    flist = data["files"]
    if fc!="전체": flist=[f for f in flist if f.get("category")==fc]
    if fk: flist=[f for f in flist if fk.lower() in f["name"].lower()]
    flist=sorted(flist,key=lambda x:x.get("uploaded_at",""),reverse=True)

    st.markdown(f"**총 {len(flist)}건**")
    if not flist: st.info("등록된 자료가 없습니다.")
    for f in flist:
        ext = f["name"].split(".")[-1].upper() if "." in f["name"] else "FILE"
        skb = f.get("size",0)//1024
        tc = "tag-blue" if ext=="PDF" else "tag-green" if ext in ["XLSX","XLS"] else "tag-orange" if ext in ["DOCX","DOC","HWP"] else "tag-gray"
        rc1,rc2,rc3 = st.columns([6,1,1])
        with rc1:
            st.markdown(f"""<div class="file-row"><div style="font-size:20px;">📄</div><div class="file-info">
              <div class="file-name">{f['name']}</div>
              <div class="file-meta"><span class="tag {tc}">{ext}</span><span class="tag tag-gray">{f.get('category','')}</span>
              {skb}KB · {f.get('uploaded_at','')[:10]}{(' · '+f['memo']) if f.get('memo') else ''}</div>
            </div></div>""",unsafe_allow_html=True)
        with rc2:
            if os.path.exists(f.get("path","")):
                with open(f["path"],"rb") as fp:
                    st.download_button("⬇️",fp.read(),file_name=f["name"],key=f"dl_{f['id']}")
        with rc3:
            if st.button("🗑️",key=f"df_{f['id']}"):
                if os.path.exists(f.get("path","")): os.remove(f["path"])
                data["files"]=[x for x in data["files"] if x["id"]!=f["id"]]
                save(data); st.rerun()

# ══════════════════ 일정 관리 ══════════════════
elif st.session_state.page == "schedule":
    st.markdown('<div class="sec-title">📅 일정 관리</div>',unsafe_allow_html=True)

    with st.expander("➕ 새 일정 등록", expanded=False):
        sc1,sc2,sc3 = st.columns([2,1,1])
        with sc1:
            st_title = st.text_input("일정 제목 *")
            st_desc  = st.text_area("상세 내용",height=80)
        with sc2:
            st_date = st.date_input("날짜 *",value=today)
            st_cat  = st.selectbox("구분",["공모/심의","협약","장비구축","SPC설립","기업지원","보고/정산","회의","교육","기타"])
        with sc3:
            st_year = st.selectbox("사업연도",["2026","2027","2028","2029","2030","해당없음"])
            st_imp  = st.selectbox("중요도",["높음 🔴","보통 🟡","낮음 🟢"])
        if st.button("📌 일정 등록",type="primary"):
            if st_title:
                data["schedules"].append({"id":int(datetime.now().timestamp()*1000),
                    "title":st_title,"description":st_desc,"date":st_date.isoformat(),
                    "category":st_cat,"year":st_year,"importance":st_imp,
                    "done":False,"created_at":datetime.now().isoformat()})
                save(data); st.success("✅ 일정 등록 완료!"); st.rerun()
            else: st.warning("일정 제목을 입력해주세요.")

    st.markdown("---")
    ff1,ff2,ff3,ff4 = st.columns(4)
    with ff1: fy=st.selectbox("사업연도",["전체","2026","2027","2028","2029","2030","해당없음"])
    with ff2: fcat=st.selectbox("구분",["전체","공모/심의","협약","장비구축","SPC설립","기업지원","보고/정산","회의","교육","기타"])
    with ff3: fst=st.selectbox("상태",["전체","미완료","완료"])
    with ff4: fsk=st.text_input("🔍 검색")

    sl = data["schedules"]
    if fy!="전체": sl=[s for s in sl if s.get("year")==fy]
    if fcat!="전체": sl=[s for s in sl if s.get("category")==fcat]
    if fst=="미완료": sl=[s for s in sl if not s.get("done")]
    if fst=="완료": sl=[s for s in sl if s.get("done")]
    if fsk: sl=[s for s in sl if fsk in s.get("title","") or fsk in s.get("description","")]
    sl=sorted(sl,key=lambda x:x.get("date",""))

    st.markdown(f"**총 {len(sl)}건**")
    tab1,tab2,tab3,tab4 = st.tabs(["📋 목록","🗓️ 달력","📆 연차별","⚡ D-Day 현황"])

    with tab1:
        if not sl: st.info("등록된 일정이 없습니다.")
        for s in sl:
            d=date.fromisoformat(s["date"]) if s.get("date") else None
            diff=(d-today).days if d else None
            if s.get("done"): badge='<span class="badge-d d-done">✅ 완료</span>'
            elif diff is None: badge=""
            elif diff<0: badge=f'<span class="badge-d d-urgent">D+{abs(diff)} 초과</span>'
            elif diff==0: badge='<span class="badge-d d-urgent">🔔 D-Day</span>'
            elif diff<=7: badge=f'<span class="badge-d d-soon">D-{diff}</span>'
            elif diff<=30: badge=f'<span class="badge-d d-ok">D-{diff}</span>'
            else: badge=f'<span class="badge-d" style="background:#f1f5f9;color:#64748b;">D-{diff}</span>'
            ic="#dc2626" if "높음" in s.get("importance","") else "#d97706" if "보통" in s.get("importance","") else "#16a34a"
            tc1,tc2,tc3=st.columns([7,1,1])
            with tc1:
                st.markdown(f"""<div class="sched-row" style="{'opacity:0.5' if s.get('done') else ''}">
                  <div class="sched-date">{s.get('date','')}</div>
                  <div><div class="sched-title"><span style="color:{ic};margin-right:4px;">●</span>{s['title']} {badge}
                    <span class="tag tag-gray" style="font-size:10px;">{s.get('category','')}</span>
                    <span class="tag tag-blue" style="font-size:10px;">{s.get('year','')}</span></div>
                  <div class="sched-desc">{s.get('description','')[:80]}</div></div>
                </div>""",unsafe_allow_html=True)
            with tc2:
                if st.button("↩️" if s.get("done") else "✅",key=f"done_{s['id']}"):
                    for item in data["schedules"]:
                        if item["id"]==s["id"]: item["done"]=not item.get("done",False)
                    save(data); st.rerun()
            with tc3:
                if st.button("🗑️",key=f"ds_{s['id']}"):
                    data["schedules"]=[x for x in data["schedules"] if x["id"]!=s["id"]]
                    save(data); st.rerun()

    with tab2:
        import calendar
        cal_col1, cal_col2 = st.columns([1,3])
        with cal_col1:
            cal_year  = st.selectbox("년도", [2026,2027,2028,2029,2030], index=max(0, today.year-2026), key="cal_y")
            cal_month = st.selectbox("월", list(range(1,13)), index=today.month-1, key="cal_m")

        # 해당 월 일정 모아두기
        month_scheds = {}
        for s in data["schedules"]:
            if s.get("date"):
                try:
                    sd = date.fromisoformat(s["date"])
                    if sd.year == cal_year and sd.month == cal_month:
                        month_scheds.setdefault(sd.day, []).append(s)
                except: pass

        with cal_col2:
            st.markdown(f"#### {cal_year}년 {cal_month}월")
            # 요일 헤더
            days_kr = ["월","화","수","목","금","토","일"]
            header_html = '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-bottom:4px;">'
            for i,d_name in enumerate(days_kr):
                color = "#2563eb" if i==5 else "#dc2626" if i==6 else "#64748b"
                header_html += f'<div style="text-align:center;font-size:12px;font-weight:700;color:{color};padding:4px;">{d_name}</div>'
            header_html += '</div>'
            st.markdown(header_html, unsafe_allow_html=True)

            # 달력 생성
            cal = calendar.monthcalendar(cal_year, cal_month)
            for week in cal:
                week_html = '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-bottom:4px;">'
                for wi, day_num in enumerate(week):
                    if day_num == 0:
                        week_html += '<div style="min-height:64px;"></div>'
                        continue
                    is_today = (day_num == today.day and cal_year == today.year and cal_month == today.month)
                    is_sat = wi == 5
                    is_sun = wi == 6
                    day_scheds = month_scheds.get(day_num, [])

                    num_color = "#2563eb" if is_sat else "#dc2626" if is_sun else "#1e293b"
                    bg = "#dbeafe" if is_today else "#fff"
                    border = "2px solid #2563eb" if is_today else "1px solid #e2e8f0"

                    dots_html = ""
                    for s in day_scheds[:3]:
                        imp = s.get("importance","")
                        dc = "#dc2626" if "높음" in imp else "#d97706" if "보통" in imp else "#16a34a"
                        if s.get("done"): dc = "#94a3b8"
                        short = s["title"][:8] + ("…" if len(s["title"])>8 else "")
                        dots_html += f'<div style="background:{dc};color:#fff;font-size:9px;border-radius:3px;padding:1px 4px;margin-top:2px;overflow:hidden;white-space:nowrap;">{short}</div>'
                    if len(day_scheds) > 3:
                        dots_html += f'<div style="font-size:9px;color:#94a3b8;margin-top:1px;">+{len(day_scheds)-3}건 더</div>'

                    week_html += f'''<div style="min-height:64px;background:{bg};border:{border};
                      border-radius:8px;padding:4px 6px;">
                      <div style="font-size:12px;font-weight:700;color:{num_color};">{day_num}</div>
                      {dots_html}
                    </div>'''
                week_html += '</div>'
                st.markdown(week_html, unsafe_allow_html=True)

        # 해당 월 일정 목록
        if month_scheds:
            st.markdown(f"**{cal_month}월 일정 목록**")
            for day_num in sorted(month_scheds.keys()):
                for s in month_scheds[day_num]:
                    imp = s.get("importance","")
                    ic = "#dc2626" if "높음" in imp else "#d97706" if "보통" in imp else "#16a34a"
                    done_style = "opacity:0.5;text-decoration:line-through;" if s.get("done") else ""
                    st.markdown(f'''<div style="display:flex;gap:10px;align-items:center;
                      padding:8px 14px;background:#fff;border:1px solid #e2e8f0;
                      border-radius:8px;margin-bottom:6px;{done_style}">
                      <span style="color:{ic};font-size:14px;">●</span>
                      <span style="font-weight:700;color:#1e3a5f;min-width:30px;">{day_num}일</span>
                      <span style="font-size:13px;color:#1e293b;">{s["title"]}</span>
                      <span class="tag tag-gray" style="font-size:10px;">{s.get("category","")}</span>
                      {"<span class='tag' style='background:#dcfce7;color:#16a34a;font-size:10px;'>✅완료</span>" if s.get("done") else ""}
                    </div>''', unsafe_allow_html=True)
        else:
            st.info(f"{cal_month}월에 등록된 일정이 없습니다.")

    with tab3:
        for yr in ["2026","2027","2028","2029","2030"]:
            ys=[s for s in data["schedules"] if s.get("year")==yr]
            dc=sum(1 for s in ys if s.get("done"))
            pct=int(dc/len(ys)*100) if ys else 0
            st.markdown(f"""<div style="display:flex;align-items:center;gap:12px;padding:10px 16px;
              background:#fff;border:1px solid #e2e8f0;border-radius:10px;margin-bottom:6px;">
              <span style="font-weight:800;color:#1e3a5f;min-width:55px;">{yr}년</span>
              <span style="font-size:12px;color:#64748b;">총 {len(ys)}건 · 완료 {dc}건</span>
              <div style="flex:1;background:#e2e8f0;border-radius:4px;height:6px;">
                <div style="width:{pct}%;background:#2563eb;border-radius:4px;height:6px;"></div></div>
              <span style="font-size:11px;color:#2563eb;font-weight:700;">{pct}%</span>
            </div>""",unsafe_allow_html=True)
            for s in sorted(ys,key=lambda x:x.get("date","")):
                chk="✅" if s.get("done") else "⬜"
                color="#94a3b8" if s.get("done") else "#1e293b"
                st.markdown(f'<div style="padding:3px 0 3px 24px;font-size:12px;color:{color};">{chk} {s.get("date","")} &nbsp; {s["title"]} <span style="color:#94a3b8;">({s.get("category","")})</span></div>',unsafe_allow_html=True)

    with tab4:
        urgent=[s for s in data["schedules"] if not s.get("done") and s.get("date")
                and (date.fromisoformat(s["date"])-today).days<=30]
        urgent=sorted(urgent,key=lambda x:x["date"])
        if not urgent: st.success("🎉 30일 내 촉박한 일정이 없습니다!")
        for s in urgent:
            d=date.fromisoformat(s["date"]); diff=(d-today).days
            if diff<0: bg="#fee2e2";lb=f"⚠️ {abs(diff)}일 초과"
            elif diff==0: bg="#fee2e2";lb="🔔 오늘"
            elif diff<=7: bg="#fef3c7";lb=f"⚡ {diff}일 후"
            else: bg="#dcfce7";lb=f"📌 {diff}일 후"
            st.markdown(f"""<div style="background:{bg};border-radius:10px;padding:12px 16px;
              margin-bottom:8px;display:flex;gap:12px;align-items:center;">
              <span style="font-size:12px;font-weight:700;min-width:80px;">{lb}</span>
              <div><div style="font-weight:700;font-size:13px;">{s['title']}</div>
              <div style="font-size:11px;color:#64748b;">{s.get('date','')} · {s.get('category','')} · {s.get('year','')}</div></div>
            </div>""",unsafe_allow_html=True)
