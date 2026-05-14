# mi_app.py
# Mixing Index (MI) Calculator - Dark Mode Premium
# 재능대학교 바이오테크과 - 남정훈 교수 (개발자)

import streamlit as st
import numpy as np
from PIL import Image
from streamlit_cropper import st_cropper
import pandas as pd
import plotly.graph_objects as go

# ===== 개발자 정보 =====
DEVELOPER_NAME = "남정훈 교수"
AFFILIATION    = "재능대학교 바이오테크과"
VERSION        = "2.2"
YEAR           = "2026"

# ===== 페이지 설정 =====
st.set_page_config(
    page_title="MI Calculator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== 다크모드 CSS =====
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: #e2e8f0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    .stApp, .stApp p, .stApp label, .stApp span, .stApp div {
        color: #e2e8f0;
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #f1f5f9 !important;
    }
    
    /* 헤더 */
    .main-header {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
        backdrop-filter: blur(20px);
        padding: 2.5rem 2rem;
        border-radius: 24px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 0 60px rgba(99, 102, 241, 0.2);
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #a78bfa 0%, #22d3ee 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    .main-header p {
        color: #cbd5e1 !important;
        font-size: 1rem;
        margin: 0.8rem 0 0 0;
        font-weight: 300;
    }
    .main-header .badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.2);
        padding: 6px 16px;
        border-radius: 20px;
        margin: 0 5px;
        font-size: 0.85rem;
        border: 1px solid rgba(99, 102, 241, 0.4);
        color: #e0e7ff !important;
    }
    
    /* 단계 제목 */
    .step-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(99, 102, 241, 0.2);
    }
    .step-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        font-weight: bold;
        margin-right: 12px;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.6);
        flex-shrink: 0;
    }
    .step-title-text {
        font-size: 1.2rem;
        font-weight: 600;
        color: #f1f5f9 !important;
        flex-grow: 1;
    }
    .status-pending {
        background: rgba(251, 191, 36, 0.15);
        color: #fbbf24 !important;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        border: 1px solid rgba(251, 191, 36, 0.3);
    }
    .status-done {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399 !important;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    /* MI 결과 카드 */
    .mi-result-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
        backdrop-filter: blur(20px);
        padding: 2.5rem 2rem;
        border-radius: 24px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 0 40px rgba(99, 102, 241, 0.2);
        text-align: center;
        margin: 1rem 0;
    }
    .mi-value-big {
        font-size: 5rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(135deg, #a78bfa, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
        letter-spacing: -2px;
    }
    .mi-label {
        font-size: 0.85rem;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    /* 버튼 */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0.7rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.6);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
    }
    
    /* 사이드바 */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }
    [data-testid="stSidebar"] h3 {
        color: #a78bfa !important;
        font-weight: 700;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] li {
        color: #cbd5e1 !important;
    }
    
    /* 사이드바 토글 버튼 - 강조 표시 */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        background: linear-gradient(135deg, #6366f1, #a855f7) !important;
        border-radius: 8px !important;
        padding: 6px !important;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.7) !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="collapsedControl"] svg {
        color: white !important;
        fill: white !important;
    }
    
    /* 메트릭 박스 */
    .metric-box {
        background: rgba(30, 41, 59, 0.6);
        padding: 1.2rem;
        border-radius: 14px;
        text-align: center;
        border: 1px solid rgba(99, 102, 241, 0.2);
        transition: all 0.3s;
    }
    .metric-box:hover {
        border-color: rgba(99, 102, 241, 0.5);
    }
    .metric-box .label {
        font-size: 0.7rem;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .metric-box .value {
        font-size: 1.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a78bfa, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 0.4rem;
    }
    
    /* 진행 표시기 */
    .progress-circle {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: rgba(30, 41, 59, 0.8);
        color: #64748b;
        line-height: 48px;
        margin: 0 auto;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s;
        border: 2px solid rgba(99, 102, 241, 0.2);
    }
    .progress-circle.active {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white;
        border-color: rgba(167, 139, 250, 0.6);
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.6);
        animation: glow 2s ease-in-out infinite;
    }
    .progress-circle.done {
        background: linear-gradient(135deg, #10b981, #06b6d4);
        color: white;
        border-color: rgba(52, 211, 153, 0.6);
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.5);
    }
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 30px rgba(99, 102, 241, 0.6); }
        50% { box-shadow: 0 0 50px rgba(167, 139, 250, 0.8); }
    }
    
    /* 파일 업로더 */
    [data-testid="stFileUploader"] {
        background: rgba(15, 23, 42, 0.5);
        border: 2px dashed rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        transition: all 0.3s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(99, 102, 241, 0.6);
    }
    [data-testid="stFileUploader"] section {
        background: transparent !important;
    }
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #6366f1, #a855f7) !important;
        color: white !important;
        border: none !important;
    }
    
    /* 데이터프레임 */
    [data-testid="stDataFrame"] {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 12px;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    /* 알림 박스 */
    [data-testid="stAlert"] {
        background: rgba(30, 41, 59, 0.6) !important;
        border-radius: 12px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #e2e8f0 !important;
    }
    
    /* 푸터 */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #64748b !important;
        font-size: 0.85rem;
        border-top: 1px solid rgba(99, 102, 241, 0.2);
        margin-top: 3rem;
    }
    .footer strong {
        background: linear-gradient(135deg, #a78bfa, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .katex { color: #e2e8f0 !important; }
    
    /* 메인 메뉴와 푸터만 숨김 (header는 사이드바 버튼 있어서 유지) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 스크롤바 */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.5); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ===== 헤더 =====
st.markdown(f"""
<div class="main-header">
    <h1>🧪 Mixing Index Calculator</h1>
    <p>✨ 마이크로믹서 혼합지수 분석 도구 ✨</p>
    <p style="margin-top:1rem;">
        <span class="badge">🏛️ {AFFILIATION}</span>
        <span class="badge">👨‍🏫 {DEVELOPER_NAME}</span>
        <span class="badge">⚡ v{VERSION} · {YEAR}</span>
    </p>
</div>
""", unsafe_allow_html=True)

# ===== 세션 상태 초기화 =====
if "I1" not in st.session_state:
    st.session_state.I1 = None
    st.session_state.I2 = None
    st.session_state.results = []

# ===== 진행 표시기 =====
step1_done = st.session_state.I1 is not None
step2_done = st.session_state.I2 is not None
step3_active = step1_done and step2_done

c1, c2, c3 = st.columns(3)
with c1:
    status = "done" if step1_done else "active"
    color = "#34d399" if step1_done else "#a78bfa"
    st.markdown(f"""
    <div style='text-align:center;'>
        <div class='progress-circle {status}'>{"✓" if step1_done else "1"}</div>
        <p style='margin-top:0.6rem;font-weight:600;color:{color} !important;letter-spacing:1px;'>SAMPLE 1</p>
    </div>
    """, unsafe_allow_html=True)
with c2:
    if step2_done:
        status = "done"; color = "#34d399"
    elif step1_done:
        status = "active"; color = "#a78bfa"
    else:
        status = ""; color = "#64748b"
    st.markdown(f"""
    <div style='text-align:center;'>
        <div class='progress-circle {status}'>{"✓" if step2_done else "2"}</div>
        <p style='margin-top:0.6rem;font-weight:600;color:{color} !important;letter-spacing:1px;'>SAMPLE 2</p>
    </div>
    """, unsafe_allow_html=True)
with c3:
    status = "active" if step3_active else ""
    color = "#a78bfa" if step3_active else "#64748b"
    st.markdown(f"""
    <div style='text-align:center;'>
        <div class='progress-circle {status}'>3</div>
        <p style='margin-top:0.6rem;font-weight:600;color:{color} !important;letter-spacing:1px;'>MIXED</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.markdown("---")

# ===== 사이드바 =====
with st.sidebar:
    st.markdown("### 📖 사용 방법")
    st.markdown("""
    **Step 1** · 순수 샘플 1 업로드 + ROI  
    **Step 2** · 순수 샘플 2 업로드 + ROI  
    **Step 3** · 혼합 이미지 업로드 + ROI  
    **Step 4** · MI 자동 계산 및 결과 확인  
    **Step 5** · CSV 다운로드
    """)
    
    st.markdown("---")
    st.markdown("### 📐 MI 계산 공식")
    st.latex(r"c = \mathrm{clip}\left(\frac{I-I_1}{I_2-I_1},\,0,\,1\right)")
    st.latex(r"\sigma = \sqrt{\frac{1}{N}\sum(c-\bar{c})^2}")
    st.latex(r"\sigma_{max} = \sqrt{\bar{c}(1-\bar{c})}")
    st.latex(r"MI = 1 - \frac{\sigma}{\sigma_{max}}")
    
    st.markdown("---")
    st.markdown("### 🎯 MI 등급")
    st.markdown("""
    🟢 **0.9 ~ 1.0** · 우수한 혼합  
    🟡 **0.7 ~ 0.9** · 양호한 혼합  
    🟠 **0.5 ~ 0.7** · 부분 혼합  
    🔴 **0.0 ~ 0.5** · 미흡한 혼합
    """)
    
    st.markdown("---")
    if st.button("🔄 전체 초기화"):
        st.session_state.I1 = None
        st.session_state.I2 = None
        st.session_state.results = []
        st.rerun()

# ===== MI 계산 함수 =====
def compute_mi(mixed_arr, I1, I2):
    denom = I2 - I1
    if abs(denom) < 1e-6:
        return None
    c = np.clip((mixed_arr - I1) / denom, 0.0, 1.0)
    c_mean = float(np.mean(c))
    sigma = float(np.sqrt(np.mean((c - c_mean) ** 2)))
    sigma_max = float(np.sqrt(c_mean * (1.0 - c_mean)))
    if sigma_max < 1e-6:
        mi = 1.0
    else:
        mi = 1.0 - sigma / sigma_max
        mi = max(0.0, min(1.0, mi))
    return mi, sigma, c_mean, sigma_max

# ===== 게이지 차트 =====
def create_gauge(mi_value):
    if mi_value >= 0.9:
        color = "#34d399"
    elif mi_value >= 0.7:
        color = "#fbbf24"
    elif mi_value >= 0.5:
        color = "#fb923c"
    else:
        color = "#f87171"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=mi_value * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'suffix': "%", 'font': {'size': 52, 'color': color, 'family': "Arial Black"}},
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 1,
                'tickcolor': "#64748b",
                'tickfont': {'color': "#94a3b8", 'size': 11}
            },
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "rgba(30, 41, 59, 0.5)",
            'borderwidth': 2,
            'bordercolor': "rgba(99, 102, 241, 0.3)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(248, 113, 113, 0.15)'},
                {'range': [50, 70], 'color': 'rgba(251, 146, 60, 0.15)'},
                {'range': [70, 90], 'color': 'rgba(251, 191, 36, 0.15)'},
                {'range': [90, 100], 'color': 'rgba(52, 211, 153, 0.15)'}
            ],
            'threshold': {
                'line': {'color': "#a78bfa", 'width': 4},
                'thickness': 0.85,
                'value': 90
            }
        }
    ))
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'family': "Arial", 'color': "#e2e8f0"}
    )
    return fig

# ===== 3개 컬럼 =====
col1, col2, col3 = st.columns(3)

with col1:
    status_html = '<span class="status-done">✓ 완료</span>' if step1_done else '<span class="status-pending">⏳ 대기</span>'
    st.markdown(f"""
    <div class="step-header">
        <span class="step-number">1</span>
        <span class="step-title-text">순수 샘플 1</span>
        {status_html}
    </div>
    """, unsafe_allow_html=True)
    
    file1 = st.file_uploader("이미지 선택", type=["png","jpg","jpeg","bmp","tif","tiff"], key="f1", label_visibility="collapsed")
    if file1:
        img1 = Image.open(file1).convert("L")
        st.caption("🖱️ ROI를 드래그로 지정하세요")
        cropped1 = st_cropper(img1.convert("RGB"), realtime_update=True,
                              box_color="#a78bfa", aspect_ratio=None, key="c1")
        if st.button("✅ 샘플 1 확정", key="b1"):
            arr1 = np.array(cropped1.convert("L"), dtype=np.float64)
            st.session_state.I1 = float(np.mean(arr1))
            st.rerun()
    
    if st.session_state.I1 is not None:
        st.markdown(f"""
        <div class="metric-box" style="margin-top:1rem;">
            <div class="label">평균 강도 I₁</div>
            <div class="value">{st.session_state.I1:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    status_html = '<span class="status-done">✓ 완료</span>' if step2_done else '<span class="status-pending">⏳ 대기</span>'
    st.markdown(f"""
    <div class="step-header">
        <span class="step-number">2</span>
        <span class="step-title-text">순수 샘플 2</span>
        {status_html}
    </div>
    """, unsafe_allow_html=True)
    
    file2 = st.file_uploader("이미지 선택", type=["png","jpg","jpeg","bmp","tif","tiff"], key="f2", label_visibility="collapsed")
    if file2:
        img2 = Image.open(file2).convert("L")
        st.caption("🖱️ ROI를 드래그로 지정하세요")
        cropped2 = st_cropper(img2.convert("RGB"), realtime_update=True,
                              box_color="#22d3ee", aspect_ratio=None, key="c2")
        if st.button("✅ 샘플 2 확정", key="b2"):
            arr2 = np.array(cropped2.convert("L"), dtype=np.float64)
            st.session_state.I2 = float(np.mean(arr2))
            st.rerun()
    
    if st.session_state.I2 is not None:
        st.markdown(f"""
        <div class="metric-box" style="margin-top:1rem;">
            <div class="label">평균 강도 I₂</div>
            <div class="value">{st.session_state.I2:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="step-header">
        <span class="step-number">3</span>
        <span class="step-title-text">혼합 이미지</span>
    </div>
    """, unsafe_allow_html=True)
    
    if not step3_active:
        st.warning("⚠️ 먼저 샘플 1과 샘플 2를 확정해주세요.")
    else:
        file3 = st.file_uploader("이미지 선택", type=["png","jpg","jpeg","bmp","tif","tiff"], key="f3", label_visibility="collapsed")
        if file3:
            img3 = Image.open(file3).convert("L")
            st.caption("🖱️ ROI를 드래그로 지정하세요")
            cropped3 = st_cropper(img3.convert("RGB"), realtime_update=True,
                                  box_color="#34d399", aspect_ratio=None, key="c3")
            if st.button("🎯 MI 계산하기", key="b3"):
                arr3 = np.array(cropped3.convert("L"), dtype=np.float64)
                result = compute_mi(arr3, st.session_state.I1, st.session_state.I2)
                if result:
                    mi, sigma, c_mean, sigma_max = result
                    st.session_state.results.append({
                        "Filename": file3.name,
                        "MI": round(mi, 4),
                        "MI(%)": round(mi*100, 2),
                        "Sigma": round(sigma, 4),
                        "Sigma_max": round(sigma_max, 4),
                        "C_mean": round(c_mean, 3),
                        "I1": round(st.session_state.I1, 2),
                        "I2": round(st.session_state.I2, 2)
                    })
                    st.rerun()

# ===== 최신 결과 =====
if st.session_state.results:
    latest = st.session_state.results[-1]
    mi_val = latest["MI"]
    
    st.markdown("---")
    st.markdown("### ✨ 최신 분석 결과")
    
    res_col1, res_col2 = st.columns([1, 1])
    
    with res_col1:
        if mi_val >= 0.9:
            grade = "🟢 우수"; grade_color = "#34d399"
        elif mi_val >= 0.7:
            grade = "🟡 양호"; grade_color = "#fbbf24"
        elif mi_val >= 0.5:
            grade = "🟠 부분"; grade_color = "#fb923c"
        else:
            grade = "🔴 미흡"; grade_color = "#f87171"
        
        st.markdown(f"""
        <div class="mi-result-card">
            <div class="mi-label">⚡ Mixing Index ⚡</div>
            <div class="mi-value-big">{mi_val:.4f}</div>
            <div style="font-size:1.6rem;color:{grade_color} !important;font-weight:700;margin-top:0.8rem;">
                {grade} · {mi_val*100:.1f}%
            </div>
            <div style="margin-top:1.2rem;color:#94a3b8 !important;font-size:0.9rem;">
                📄 {latest['Filename']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="label">σ</div>
                <div class="value">{latest['Sigma']:.4f}</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="label">σ max</div>
                <div class="value">{latest['Sigma_max']:.4f}</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="label">c̄</div>
                <div class="value">{latest['C_mean']:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with res_col2:
        st.plotly_chart(create_gauge(mi_val), use_container_width=True)

# ===== 누적 결과 =====
st.markdown("---")
st.markdown("### 📊 누적 분석 결과")

if st.session_state.results:
    df = pd.DataFrame(st.session_state.results)
    st.dataframe(df, use_container_width=True)
    
    if len(df) > 1:
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=list(range(1, len(df)+1)),
            y=df["MI"],
            mode='lines+markers',
            line=dict(color='#a78bfa', width=3),
            marker=dict(size=14, color='#22d3ee', line=dict(color='#a78bfa', width=2)),
            name='MI',
            fill='tozeroy',
            fillcolor='rgba(167, 139, 250, 0.1)'
        ))
        fig_trend.add_hline(
            y=0.9, line_dash="dash", line_color="#34d399",
            annotation_text="우수 기준 (0.9)",
            annotation_font_color="#34d399"
        )
        fig_trend.update_layout(
            title=dict(text="MI 값 추이", font=dict(color="#f1f5f9", size=18)),
            xaxis_title="측정 순서",
            yaxis_title="Mixing Index",
            yaxis_range=[0, 1.05],
            height=380,
            plot_bgcolor="rgba(30, 41, 59, 0.3)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Arial", size=12, color="#cbd5e1"),
            xaxis=dict(gridcolor="rgba(99, 102, 241, 0.2)", color="#cbd5e1"),
            yaxis=dict(gridcolor="rgba(99, 102, 241, 0.2)", color="#cbd5e1")
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    csv = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button("📥 CSV로 다운로드", csv, "MI_results.csv", "text/csv")
else:
    st.info("💡 아직 분석 결과가 없습니다. 위 3단계를 순서대로 진행해주세요.")

# ===== 푸터 =====
st.markdown(f"""
<div class="footer">
    © {YEAR} <strong>{DEVELOPER_NAME}</strong> · {AFFILIATION}<br>
    <span style="font-size:0.8rem;color:#64748b;">Mixing Index Calculator · v{VERSION}</span>
</div>
""", unsafe_allow_html=True)
