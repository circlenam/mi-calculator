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
    initial_sidebar_state="collapsed"
)

# ============================================================
# 커스텀 CSS
# ============================================================
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

[data-testid="stHeader"] {
    background: transparent !important;
    height: 0px !important;
}

[data-testid="stToolbar"],
[data-testid="stToolbarActions"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.stAppToolbar,
.stAppDeployButton,
.stActionButton {
    visibility: hidden !important;
    display: none !important;
}

[data-testid="stSidebar"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
section[data-testid="stSidebar"] {
    display: none !important;
    visibility: hidden !important;
    width: 0px !important;
}

.main .block-container {
    max-width: 100% !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    padding-top: 2rem !important;
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    color: #e2e8f0;
}

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

/* 진행 단계 라인 (좌측 = 동그라미, 우측 = 버튼) */
.progress-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 1.5rem 0 2rem 0;
    padding: 0 1rem;
}
.progress-circles {
    display: flex;
    gap: 2rem;
    flex: 1;
    justify-content: center;
    margin-left: 150px; /* 버튼 너비만큼 보정해서 가운데 정렬 유지 */
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

.step-header {
    color: #c4b5fd !important;
    font-size: 1.3rem;
    font-weight: 600;
    border-bottom: 2px solid rgba(168, 85, 247, 0.4);
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

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

[data-testid="stFileUploader"] {
    background: rgba(30, 27, 75, 0.4);
    border: 2px dashed rgba(168, 85, 247, 0.4);
    border-radius: 12px;
    padding: 0.5rem;
}

[data-testid="stExpander"] {
    background: rgba(30, 27, 75, 0.4);
    border: 1px solid rgba(168, 85, 247, 0.3);
    border-radius: 12px;
}
[data-testid="stExpander"] summary {
    color: #c4b5fd !important;
    font-weight: 600;
}

.stDataFrame {
    background: rgba(30, 27, 75, 0.4);
    border-radius: 10px;
}

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
# 헤더
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🧪 Mixing Index (MI) Calculator</h1>
    <p>재능대학교 바이오테크과 | 남정훈 교수 | v1.3 (2026)</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 진행 단계 + 우측 초기화 버튼 (같은 라인)
# ============================================================
step1_class = "progress-done" if st.session_state.I1 is not None else "progress-active"
step2_class = "progress-done" if st.session_state.I2 is not None else ("progress-active" if st.session_state.I1 is not None else "progress-pending")
step3_class = "progress-active" if (st.session_state.I1 is not None and st.session_state.I2 is not None) else "progress-pending"

prog_col1, prog_col2, prog_col3 = st.columns([1, 4, 1])

with prog_col2:
    st.markdown(f"""
    <div style="display:flex; justify-content:center; gap:2rem; align-items:center; padding-top:0.5rem;">
        <div class="progress-circle {step1_class}">1</div>
        <div class="progress-circle {step2_class}">2</div>
        <div class="progress-circle {step3_class}">3</div>
    </div>
    """, unsafe_allow_html=True)

with prog_col3:
    if st.button("🔄 전체 초기화", key="reset_top", use_container_width=True):
        st.session_state.I1 = None
        st.session_state.I2 = None
        st.session_state.results = []
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

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

def create_trend_chart(results):
    """MI 변화 추이 라인 차트"""
    df = pd.DataFrame(results)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(1, len(df) + 1)),
        y=df["MI"] * 100,
        mode='lines+markers',
        line=dict(color='#a78bfa', width=3),
        marker=dict(size=10, color='#06b6d4', line=dict(color='#a78bfa', width=2)),
        name='MI (%)',
        hovertemplate='측정 %{x}<br>MI: %{y:.2f}%<extra></extra>'
    ))
    # 기준선
    fig.add_hline(y=90, line_dash="dash", line_color="rgba(16,185,129,0.5)", annotation_text="우수 (90%)", annotation_font_color="#10b981")
    fig.add_hline(y=70, line_dash="dash", line_color="rgba(6,182,212,0.5)", annotation_text="양호 (70%)", annotation_font_color="#06b6d4")
    fig.add_hline(y=50, line_dash="dash", line_color="rgba(234,179,8,0.5)", annotation_text="부분 (50%)", annotation_font_color="#eab308")
    
    fig.update_layout(
        title=dict(text="📈 MI 변화 추이", font=dict(color='#c4b5fd', size=18)),
        xaxis=dict(title="측정 순서", color='#94a3b8', gridcolor='rgba(168,85,247,0.1)'),
        yaxis=dict(title="MI (%)", color='#94a3b8', gridcolor='rgba(168,85,247,0.1)', range=[0, 105]),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(30,27,75,0.3)',
        height=350,
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(color='#e2e8f0')
    )
    return fig

# ============================================================
# 3단계 워크플로우
# ============================================================
col1, col2, col3 = st.columns(3)

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
# 최신 결과 카드 (Gauge 포함)
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
# 누적 결과 + 트렌드 차트
# ============================================================
if st.session_state.results:
    st.markdown("---")
    st.markdown('<div class="step-header">📋 누적 분석 결과</div>', unsafe_allow_html=True)
    df = pd.DataFrame(st.session_state.results)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 측정이 2개 이상이면 트렌드 차트 표시
    if len(st.session_state.results) >= 2:
        st.plotly_chart(create_trend_chart(st.session_state.results), use_container_width=True)
    
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 CSV 다운로드",
        csv,
        file_name="MI_results.csv",
        mime="text/csv"
    )

# ============================================================
# 사용법 / 공식 / 등급 안내
# ============================================================
st.markdown("---")

exp_col1, exp_col2, exp_col3 = st.columns(3)

with exp_col1:
    with st.expander("📖 사용법"):
        st.markdown("""
        **Step 1.** Sample 1 (미혼합 A) 이미지 업로드 → ROI 선택 → **I₁ 확정**  
        **Step 2.** Sample 2 (미혼합 B) 이미지 업로드 → ROI 선택 → **I₂ 확정**  
        **Step 3.** 혼합 이미지 업로드 → ROI 선택 → **MI 계산** 클릭
        """)

with exp_col2:
    with st.expander("📐 MI 공식"):
        st.latex(r"MI = 1 - \frac{\sigma}{\sigma_{max}}")
        st.latex(r"\sigma_{max} = \sqrt{\bar{c}(1-\bar{c})}")
        st.markdown("σ: ROI 내 농도 표준편차 | c̄: 평균 농도")

with exp_col3:
    with st.expander("🎯 MI 등급"):
        st.markdown("""
        - 🟢 **0.9 ~ 1.0** : 우수 혼합  
        - 🔵 **0.7 ~ 0.9** : 양호 혼합  
        - 🟡 **0.5 ~ 0.7** : 부분 혼합  
        - 🔴 **0.0 ~ 0.5** : 불량 혼합
        """)

# ============================================================
# 푸터
# ============================================================
st.markdown("""
<div class="footer">
    © 2026 남정훈 교수 | 재능대학교 바이오테크과 | MI Calculator v1.3
</div>
""", unsafe_allow_html=True)
