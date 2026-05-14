import streamlit as st
import numpy as np
from PIL import Image
from streamlit_cropper import st_cropper
import pandas as pd
import plotly.graph_objects as go

# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="MI Calculator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 커스텀 CSS (다크모드 + 보라/시안 네온)
# ============================================================
st.markdown("""
<style>
/* ===== 기본 Streamlit UI 정리 ===== */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* 상단 바 투명화 (사이드바 토글 버튼은 유지) */
[data-testid="stHeader"] {
    background: transparent !important;
    backdrop-filter: blur(0px) !important;
}

/* Fork 버튼 및 우측 툴바 숨기기 */
[data-testid="stToolbar"] {
    visibility: hidden !important;
    display: none !important;
}
[data-testid="stDecoration"] {
    display: none !important;
}
.stAppToolbar {
    display: none !important;
}
.stAppDeployButton {
    display: none !important;
}

/* 사이드바 토글 버튼 - 보라색 강조 */
[data-testid="stSidebarCollapsedControl"] {
    background: linear-gradient(135deg, #6366f1, #a855f7) !important;
    border-radius: 8px !important;
    box-shadow: 0 0 15px rgba(168, 85, 247, 0.6) !important;
    padding: 4px !important;
}
[data-testid="stSidebarCollapsedControl"] button svg,
[data-testid="stSidebarCollapsedControl"] svg {
    color: white !important;
    fill: white !important;
}

/* ===== 전체 배경 (다크 그라데이션) ===== */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    color: #e2e8f0;
}

/* ===== 사이드바 ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1b4b 0%, #0f172a 100%);
    border-right: 1px solid rgba(168, 85, 247, 0.2);
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* ===== 헤더 카드 ===== */
.main-header {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #06b6d4 100%);
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(168, 85, 247, 0.3);
}
.main-header h1 {
    color: white !important;
    font-size: 2.4rem;
    margin: 0;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}
.main-header p {
    color: rgba(255,255,255,0.9) !important;
    margin-top: 0.5rem;
    font-size: 1rem;
}

/* ===== 진행 단계 (Progress Circles) ===== */
.progress-container {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin: 1.5rem 0 2rem 0;
}
.progress-circle {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: white;
    font-size: 1.1rem;
}
.progress-active {
    background: linear-gradient(135deg, #6366f1, #a855f7);
    box-shadow: 0 0 20px rgba(168, 85, 247, 0.6);
}
.progress-done {
    background: linear-gradient(135deg, #06b6d4, #10b981);
    box-shadow: 0 0 15px rgba(16, 185, 129, 0.5);
}
.progress-pending {
    background: #334155;
    color: #94a3b8;
}

/* ===== 스텝 헤더 ===== */
.step-header {
    color: #c4b5fd !important;
    font-size: 1.3rem;
    font-weight: 600;
    border-bottom: 2px solid rgba(168, 85, 247, 0.4);
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

/* ===== 메트릭 카드 ===== */
.metric-box {
    background: rgba(30, 27, 75, 0.6);
    border: 1px solid rgba(168, 85, 247, 0.3);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    backdrop-filter: blur(10px);
}
.metric-label {
    color: #94a3b8;
    font-size: 0.85rem;
    margin-bottom: 0.3rem;
}
.metric-value {
    color: #a78bfa;
    font-size: 1.5rem;
    font-weight: bold;
}

/* ===== MI 결과 카드 ===== */
.result-card {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(168, 85, 247, 0.15));
    border: 1px solid rgba(168, 85, 247, 0.4);
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
    backdrop-filter: blur(10px);
}
.mi-value {
    font-size: 3.5rem;
    font-weight: bold;
    background: linear-gradient(135deg, #a78bfa, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}
.mi-grade {
    text-align: center;
    font-size: 1.2rem;
    color: #c4b5fd;
    margin-top: 0.5rem;
}

/* ===== 버튼 ===== */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #a855f7);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(168, 85, 247, 0.5);
}

/* ===== 파일 업로더 ===== */
[data-testid="stFileUploader"] {
    background: rgba(30, 27, 75, 0.4);
    border: 2px dashed rgba(168, 85, 247, 0.4);
    border-radius: 12px;
    padding: 0.5rem;
}

/* ===== 데이터프레임 ===== */
.stDataFrame {
    background: rgba(30, 27, 75, 0.4);
    border-radius: 10px;
}

/* ===== 푸터 ===== */
.footer {
    text-align: center;
    color: #64748b;
    padding: 2rem 0 1rem 0;
    margin-top: 3rem;
    border-top: 1px solid rgba(168, 85, 247, 0.2);
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 세션 상태 초기화
# ============================================================
if "I1" not in st.session_state:
    st.session_state.I1 = None
if "I2" not in st.session_state:
    st.session_state.I2 = None
if "results" not in st.session_state:
    st.session_state.results = []

# ============================================================
# 사이드바 (사용법)
# ============================================================
with st.sidebar:
    st.markdown("### 📖 사용법")
    st.markdown("""
    **Step 1.** Sample 1 (미혼합 A) 이미지 업로드 → ROI 선택 → I₁ 확정  
    **Step 2.** Sample 2 (미혼합 B) 이미지 업로드 → ROI 선택 → I₂ 확정  
    **Step 3.** 혼합 이미지 업로드 → ROI 선택 → **MI 계산** 클릭  
    """)
    
    st.markdown("---")
    st.markdown("### 📐 MI 공식")
    st.latex(r"MI = 1 - \frac{\sigma}{\sigma_{max}}")
    st.latex(r"\sigma_{max} = \sqrt{\bar{c}(1-\bar{c})}")
    
    st.markdown("---")
    st.markdown("### 🎯 MI 등급")
    st.markdown("""
    - 🟢 **0.9 ~ 1.0** : 우수 혼합  
    - 🔵 **0.7 ~ 0.9** : 양호 혼합  
    - 🟡 **0.5 ~ 0.7** : 부분 혼합  
    - 🔴 **0.0 ~ 0.5** : 불량 혼합
    """)
    
    st.markdown("---")
    if st.button("🔄 전체 초기화"):
        st.session_state.I1 = None
        st.session_state.I2 = None
        st.session_state.results = []
        st.rerun()

# ============================================================
# 헤더
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🧪 Mixing Index (MI) Calculator</h1>
    <p>재능대학교 바이오테크과 | 남정훈 교수 | v1.2 (2026)</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 진행 단계 표시
# ============================================================
step1_class = "progress-done" if st.session_state.I1 is not None else "progress-active"
step2_class = "progress-done" if st.session_state.I2 is not None else ("progress-active" if st.session_state.I1 is not None else "progress-pending")
step3_class = "progress-active" if (st.session_state.I1 is not None and st.session_state.I2 is not None) else "progress-pending"

st.markdown(f"""
<div class="progress-container">
    <div class="progress-circle {step1_class}">1</div>
    <div class="progress-circle {step2_class}">2</div>
    <div class="progress-circle {step3_class}">3</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# MI 계산 함수
# ============================================================
def compute_mi(mixed_arr, I1, I2):
    denom = I2 - I1
    if abs(denom) < 1e-6:
        return 0.0, 0.0, 0.0, 0.0
    c = (mixed_arr - I1) / denom
    c = np.clip(c, 0.0, 1.0)
    c_mean = float(np.mean(c))
    sigma = float(np.sqrt(np.mean((c - c_mean) ** 2)))
    sigma_max = float(np.sqrt(c_mean * (1.0 - c_mean)))
    if sigma_max < 1e-6:
        return 1.0, sigma, sigma_max, c_mean
    mi = 1.0 - sigma / sigma_max
    return max(0.0, min(1.0, mi)), sigma, sigma_max, c_mean

def get_grade(mi):
    if mi >= 0.9: return "🟢 우수 혼합", "#10b981"
    elif mi >= 0.7: return "🔵 양호 혼합", "#06b6d4"
    elif mi >= 0.5: return "🟡 부분 혼합", "#eab308"
    else: return "🔴 불량 혼합", "#ef4444"

def create_gauge(mi):
    _, color = get_grade(mi)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=mi * 100,
        number={'suffix': "%", 'font': {'color': '#e2e8f0', 'size': 36}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#94a3b8', 'tickfont': {'color': '#94a3b8'}},
            'bar': {'color': color},
            'bgcolor': 'rgba(30,27,75,0.3)',
            'borderwidth': 2,
            'bordercolor': 'rgba(168,85,247,0.3)',
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239,68,68,0.2)'},
                {'range': [50, 70], 'color': 'rgba(234,179,8,0.2)'},
                {'range': [70, 90], 'color': 'rgba(6,182,212,0.2)'},
                {'range': [90, 100], 'color': 'rgba(16,185,129,0.2)'},
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=280,
        margin=dict(l=20, r=20, t=30, b=20),
        font={'color': '#e2e8f0'}
    )
    return fig

# ============================================================
# 3단계 워크플로우
# ============================================================
col1, col2, col3 = st.columns(3)

# --- Step 1: Sample 1 ---
with col1:
    st.markdown('<div class="step-header">📤 Step 1. Sample 1 (I₁)</div>', unsafe_allow_html=True)
    f1 = st.file_uploader("미혼합 A 이미지", type=["png","jpg","jpeg","bmp","tif"], key="f1")
    if f1:
        img1 = Image.open(f1).convert("L")
        crop1 = st_cropper(img1, realtime_update=True, box_color="#a855f7", aspect_ratio=None, key="c1")
        if st.button("✅ I₁ 확정", key="b1"):
            arr = np.array(crop1)
            st.session_state.I1 = float(np.mean(arr))
            st.success(f"I₁ = {st.session_state.I1:.2f}")
            st.rerun()
    if st.session_state.I1 is not None:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">I₁ (Sample 1 평균)</div>
            <div class="metric-value">{st.session_state.I1:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Step 2: Sample 2 ---
with col2:
    st.markdown('<div class="step-header">📤 Step 2. Sample 2 (I₂)</div>', unsafe_allow_html=True)
    f2 = st.file_uploader("미혼합 B 이미지", type=["png","jpg","jpeg","bmp","tif"], key="f2")
    if f2:
        img2 = Image.open(f2).convert("L")
        crop2 = st_cropper(img2, realtime_update=True, box_color="#06b6d4", aspect_ratio=None, key="c2")
        if st.button("✅ I₂ 확정", key="b2"):
            arr = np.array(crop2)
            st.session_state.I2 = float(np.mean(arr))
            st.success(f"I₂ = {st.session_state.I2:.2f}")
            st.rerun()
    if st.session_state.I2 is not None:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">I₂ (Sample 2 평균)</div>
            <div class="metric-value">{st.session_state.I2:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Step 3: Mixed Image ---
with col3:
    st.markdown('<div class="step-header">🔬 Step 3. 혼합 이미지</div>', unsafe_allow_html=True)
    if st.session_state.I1 is None or st.session_state.I2 is None:
        st.info("Step 1, 2를 먼저 완료하세요.")
    else:
        f3 = st.file_uploader("혼합 이미지", type=["png","jpg","jpeg","bmp","tif"], key="f3")
        if f3:
            img3 = Image.open(f3).convert("L")
            crop3 = st_cropper(img3, realtime_update=True, box_color="#10b981", aspect_ratio=None, key="c3")
            if st.button("🧮 MI 계산", key="b3"):
                arr = np.array(crop3)
                mi, sigma, sigma_max, c_mean = compute_mi(arr, st.session_state.I1, st.session_state.I2)
                st.session_state.results.append({
                    "파일명": f3.name,
                    "MI": round(mi, 4),
                    "σ": round(sigma, 4),
                    "σ_max": round(sigma_max, 4),
                    "c̄": round(c_mean, 4),
                    "I₁": round(st.session_state.I1, 2),
                    "I₂": round(st.session_state.I2, 2),
                })
                st.rerun()

# ============================================================
# 최신 결과 카드
# ============================================================
if st.session_state.results:
    latest = st.session_state.results[-1]
    grade_text, _ = get_grade(latest["MI"])
    
    st.markdown("---")
    st.markdown('<div class="step-header">📊 최신 분석 결과</div>', unsafe_allow_html=True)
    
    res_col1, res_col2 = st.columns([1, 1])
    
    with res_col1:
        st.markdown(f"""
        <div class="result-card">
            <div style="text-align:center; color:#94a3b8;">Mixing Index</div>
            <div class="mi-value">{latest['MI']*100:.1f}%</div>
            <div class="mi-grade">{grade_text}</div>
            <hr style="border-color: rgba(168,85,247,0.2); margin: 1rem 0;">
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem;">
                <div class="metric-box"><div class="metric-label">σ</div><div class="metric-value" style="font-size:1.1rem;">{latest['σ']:.4f}</div></div>
                <div class="metric-box"><div class="metric-label">σ_max</div><div class="metric-value" style="font-size:1.1rem;">{latest['σ_max']:.4f}</div></div>
                <div class="metric-box"><div class="metric-label">c̄</div><div class="metric-value" style="font-size:1.1rem;">{latest['c̄']:.4f}</div></div>
                <div class="metric-box"><div class="metric-label">파일</div><div class="metric-value" style="font-size:0.85rem;">{latest['파일명'][:15]}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with res_col2:
        st.plotly_chart(create_gauge(latest["MI"]), use_container_width=True)

# ============================================================
# 누적 결과 테이블
# ============================================================
if st.session_state.results:
    st.markdown("---")
    st.markdown('<div class="step-header">📋 누적 분석 결과</div>', unsafe_allow_html=True)
    df = pd.DataFrame(st.session_state.results)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 CSV 다운로드",
        csv,
        file_name="MI_results.csv",
        mime="text/csv"
    )

# ============================================================
# 푸터
# ============================================================
st.markdown("""
<div class="footer">
    © 2026 남정훈 교수 | 재능대학교 바이오테크과 | MI Calculator v1.2
</div>
""", unsafe_allow_html=True)
