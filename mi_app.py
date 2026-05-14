# mi_app.py
# Mixing Index (MI) Calculator - Modern Web Version
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
VERSION        = "2.0"
YEAR           = "2026"

# ===== 페이지 설정 =====
st.set_page_config(
    page_title="MI Calculator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== 커스텀 CSS =====
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8edf3 100%);
    }
    
    /* 메인 컨테이너 패딩 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* 헤더 스타일 */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1rem;
        margin: 0.8rem 0 0 0;
        font-weight: 300;
    }
    .main-header .badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 4px 14px;
        border-radius: 20px;
        margin: 0 5px;
        font-size: 0.85rem;
        backdrop-filter: blur(10px);
    }
    
    /* 카드 스타일 */
    .step-card {
        background: white;
        padding: 1.8rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-top: 4px solid #667eea;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .step-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    .step-number {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        text-align: center;
        line-height: 32px;
        font-weight: bold;
        margin-right: 10px;
    }
    .step-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
    }
    
    /* 상태 배지 */
    .status-pending {
        background: #fef3c7;
        color: #92400e;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
    }
    .status-done {
        background: #d1fae5;
        color: #065f46;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
    }
    
    /* MI 결과 카드 */
    .mi-result-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1rem 0;
    }
    .mi-value-big {
        font-size: 4rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }
    .mi-label {
        font-size: 0.9rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.5rem;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* 다운로드 버튼 */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    /* 사이드바 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f9fafb 100%);
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    
    /* 메트릭 박스 */
    .metric-box {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-left: 4px solid #667eea;
    }
    .metric-box .label {
        font-size: 0.75rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-box .value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2d3748;
        margin-top: 0.3rem;
    }
    
    /* 진행 표시기 */
    .progress-bar {
        display: flex;
        justify-content: space-between;
        margin-bottom: 2rem;
        position: relative;
    }
    .progress-step {
        flex: 1;
        text-align: center;
        position: relative;
    }
    .progress-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #e5e7eb;
        color: #9ca3af;
        line-height: 40px;
        margin: 0 auto;
        font-weight: bold;
        transition: all 0.3s;
    }
    .progress-circle.active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    }
    .progress-circle.done {
        background: #10b981;
        color: white;
    }
    
    /* 푸터 */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #6b7280;
        font-size: 0.85rem;
        border-top: 1px solid #e5e7eb;
        margin-top: 3rem;
    }
    
    /* 헤더 숨김 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ===== 헤더 =====
st.markdown(f"""
<div class="main-header">
    <h1>🧪 Mixing Index Calculator</h1>
    <p>마이크로믹서 혼합지수 분석 도구</p>
    <p style="margin-top:1rem;">
        <span class="badge">🏛️ {AFFILIATION}</span>
        <span class="badge">👨‍🏫 {DEVELOPER_NAME}</span>
        <span class="badge">v{VERSION} ({YEAR})</span>
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
    st.markdown(f"""
    <div style='text-align:center;'>
        <div class='progress-circle {status}'>{"✓" if step1_done else "1"}</div>
        <p style='margin-top:0.5rem;font-weight:500;color:{"#10b981" if step1_done else "#667eea"};'>샘플 1</p>
    </div>
    """, unsafe_allow_html=True)
with c2:
    if step2_done:
        status = "done"
    elif step1_done:
        status = "active"
    else:
        status = ""
    st.markdown(f"""
    <div style='text-align:center;'>
        <div class='progress-circle {status}'>{"✓" if step2_done else "2"}</div>
        <p style='margin-top:0.5rem;font-weight:500;color:{"#10b981" if step2_done else "#667eea" if step1_done else "#9ca3af"};'>샘플 2</p>
    </div>
    """, unsafe_allow_html=True)
with c3:
    status = "active" if step3_active else ""
    st.markdown(f"""
    <div style='text-align:center;'>
        <div class='progress-circle {status}'>3</div>
        <p style='margin-top:0.5rem;font-weight:500;color:{"#667eea" if step3_active else "#9ca3af"};'>혼합 이미지</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ===== 사이드바 =====
with st.sidebar:
    st.markdown("### 📖 사용 방법")
    st.markdown("""
    **Step 1.** 순수 샘플 1 이미지 업로드 후 ROI 지정  
    **Step 2.** 순수 샘플 2 이미지 업로드 후 ROI 지정  
    **Step 3.** 혼합 이미지 업로드 후 ROI 지정 → MI 계산  
    **Step 4.** 결과를 CSV로 다운로드
    """)
    
    st.markdown("---")
    st.markdown("### 📐 MI 계산 공식")
    st.latex(r"c = \mathrm{clip}\left(\frac{I-I_1}{I_2-I_1},\,0,\,1\right)")
    st.latex(r"\sigma = \sqrt{\frac{1}{N}\sum(c-\bar{c})^2}")
    st.latex(r"\sigma_{max} = \sqrt{\bar{c}(1-\bar{c})}")
    st.latex(r"MI = 1 - \frac{\sigma}{\sigma_{max}}")
    
    st.markdown("---")
    st.markdown("### 🎯 MI 해석")
    st.markdown("""
    - 🟢 **0.9 ~ 1.0**: 우수한 혼합
    - 🟡 **0.7 ~ 0.9**: 양호한 혼합
    - 🟠 **0.5 ~ 0.7**: 부분 혼합
    - 🔴 **0.0 ~ 0.5**: 미흡한 혼합
    """)
    
    st.markdown("---")
    if st.button("🔄 초기화"):
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

# ===== 게이지 차트 함수 =====
def create_gauge(mi_value):
    if mi_value >= 0.9:
        color = "#10b981"
    elif mi_value >= 0.7:
        color = "#f59e0b"
    elif mi_value >= 0.5:
        color = "#fb923c"
    else:
        color = "#ef4444"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=mi_value * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'suffix': "%", 'font': {'size': 48, 'color': color}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#9ca3af"},
            'bar': {'color': color, 'thickness': 0.8},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e5e7eb",
            'steps': [
                {'range': [0, 50], 'color': '#fee2e2'},
                {'range': [50, 70], 'color': '#fed7aa'},
                {'range': [70, 90], 'color': '#fef3c7'},
                {'range': [90, 100], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': "#1f2937", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'family': "Arial"}
    )
    return fig

# ===== 3개 컬럼 레이아웃 =====
col1, col2, col3 = st.columns(3)

# ----- 샘플 1 -----
with col1:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    status_html = '<span class="status-done">✓ 완료</span>' if step1_done else '<span class="status-pending">대기 중</span>'
    st.markdown(f"""
    <div class="step-title">
        <span class="step-number">1</span>순수 샘플 1 {status_html}
    </div>
    """, unsafe_allow_html=True)
    
    file1 = st.file_uploader("이미지 선택", type=["png","jpg","jpeg","bmp","tif","tiff"], key="f1", label_visibility="collapsed")
    if file1:
        img1 = Image.open(file1).convert("L")
        st.caption("🖱️ ROI를 드래그로 지정하세요")
        cropped1 = st_cropper(img1.convert("RGB"), realtime_update=True,
                              box_color="#667eea", aspect_ratio=None, key="c1")
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
    st.markdown('</div>', unsafe_allow_html=True)

# ----- 샘플 2 -----
with col2:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    status_html = '<span class="status-done">✓ 완료</span>' if step2_done else '<span class="status-pending">대기 중</span>'
    st.markdown(f"""
    <div class="step-title">
        <span class="step-number">2</span>순수 샘플 2 {status_html}
    </div>
    """, unsafe_allow_html=True)
    
    file2 = st.file_uploader("이미지 선택", type=["png","jpg","jpeg","bmp","tif","tiff"], key="f2", label_visibility="collapsed")
    if file2:
        img2 = Image.open(file2).convert("L")
        st.caption("🖱️ ROI를 드래그로 지정하세요")
        cropped2 = st_cropper(img2.convert("RGB"), realtime_update=True,
                              box_color="#764ba2", aspect_ratio=None, key="c2")
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
    st.markdown('</div>', unsafe_allow_html=True)

# ----- 혼합 이미지 -----
with col3:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="step-title">
        <span class="step-number">3</span>혼합 이미지
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
                                  box_color="#10b981", aspect_ratio=None, key="c3")
            if st.button("🎯 MI 계산", key="b3"):
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
    st.markdown('</div>', unsafe_allow_html=True)

# ===== 최신 결과 표시 =====
if st.session_state.results:
    latest = st.session_state.results[-1]
    mi_val = latest["MI"]
    
    st.markdown("---")
    st.markdown("### 🎯 최신 분석 결과")
    
    res_col1, res_col2 = st.columns([1, 1])
    
    with res_col1:
        # 등급 결정
        if mi_val >= 0.9:
            grade = "🟢 우수"
            grade_color = "#10b981"
        elif mi_val >= 0.7:
            grade = "🟡 양호"
            grade_color = "#f59e0b"
        elif mi_val >= 0.5:
            grade = "🟠 부분"
            grade_color = "#fb923c"
        else:
            grade = "🔴 미흡"
            grade_color = "#ef4444"
        
        st.markdown(f"""
        <div class="mi-result-card">
            <div class="mi-label">Mixing Index</div>
            <div class="mi-value-big">{mi_val:.4f}</div>
            <div style="font-size:1.5rem;color:{grade_color};font-weight:600;margin-top:0.5rem;">
                {grade} ({mi_val*100:.1f}%)
            </div>
            <div style="margin-top:1rem;color:#6b7280;font-size:0.9rem;">
                📄 {latest['Filename']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 세부 메트릭
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
                <div class="label">σ_max</div>
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

# ===== 누적 결과 테이블 =====
st.markdown("---")
st.markdown("### 📊 누적 분석 결과")

if st.session_state.results:
    df = pd.DataFrame(st.session_state.results)
    st.dataframe(df, use_container_width=True, hide_index=False)
    
    # MI 추이 그래프
    if len(df) > 1:
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=list(range(1, len(df)+1)),
            y=df["MI"],
            mode='lines+markers',
            line=dict(color='#667eea', width=3),
            marker=dict(size=12, color='#764ba2', line=dict(color='white', width=2)),
            name='MI'
        ))
        fig_trend.add_hline(y=0.9, line_dash="dash", line_color="#10b981", 
                           annotation_text="우수 기준 (0.9)")
        fig_trend.update_layout(
            title="MI 값 추이",
            xaxis_title="측정 순서",
            yaxis_title="Mixing Index",
            yaxis_range=[0, 1.05],
            height=350,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Arial", size=12)
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
    <span style="font-size:0.8rem;">Mixing Index Calculator v{VERSION}</span>
</div>
""", unsafe_allow_html=True)
