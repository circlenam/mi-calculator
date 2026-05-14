# mi_app.py
# Mixing Index (MI) Calculator - Web Version
# 재능대학교 바이오테크과 - 남정훈 교수 (개발자)

import streamlit as st
import numpy as np
from PIL import Image
from streamlit_cropper import st_cropper
import pandas as pd
import io

# ===== 개발자 정보 =====
DEVELOPER_NAME = "남정훈 교수"
AFFILIATION    = "재능대학교 바이오테크과"
VERSION        = "1.1"
YEAR           = "2026"

st.set_page_config(page_title="MI Calculator", page_icon="🧪", layout="wide")

# ===== 헤더 =====
st.markdown(
    f"""
    <div style='background-color:#003366;padding:15px;border-radius:5px;text-align:center;'>
        <h2 style='color:white;margin:0;'>Mixing Index (MI) Calculator</h2>
        <p style='color:white;margin:5px 0 0 0;'>
            {AFFILIATION} | {DEVELOPER_NAME} (개발자) | v{VERSION} ({YEAR})
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("")

# ===== 세션 상태 초기화 =====
if "I1" not in st.session_state:
    st.session_state.I1 = None
    st.session_state.I2 = None
    st.session_state.results = []

# ===== 사이드바: 사용 방법 =====
with st.sidebar:
    st.header("📖 사용 방법")
    st.markdown("""
    1. **샘플 1** 이미지 업로드 → ROI 지정 → 확정
    2. **샘플 2** 이미지 업로드 → ROI 지정 → 확정
    3. **혼합 이미지** 업로드 → ROI 지정 → MI 계산
    4. 여러 혼합 이미지 반복 분석 가능
    5. 결과를 CSV로 다운로드
    """)
    st.markdown("---")
    st.subheader("📐 MI 계산 공식")
    st.latex(r"c = \mathrm{clip}\left(\frac{I-I_1}{I_2-I_1},\,0,\,1\right)")
    st.latex(r"\sigma = \sqrt{\frac{1}{N}\sum(c-\bar{c})^2}")
    st.latex(r"\sigma_{max} = \sqrt{\bar{c}(1-\bar{c})}")
    st.latex(r"MI = 1 - \frac{\sigma}{\sigma_{max}}")
    st.markdown("---")
    if st.button("🔄 초기화 (전체 리셋)"):
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

# ===== 3개 컬럼 레이아웃 =====
col1, col2, col3 = st.columns(3)

# ----- 샘플 1 -----
with col1:
    st.subheader("Step 1: 순수 샘플 1")
    file1 = st.file_uploader("샘플 1 이미지", type=["png","jpg","jpeg","bmp","tif","tiff"], key="f1")
    if file1:
        img1 = Image.open(file1).convert("L")
        st.write("ROI를 드래그로 지정하세요:")
        cropped1 = st_cropper(img1.convert("RGB"), realtime_update=True,
                              box_color="#FF0000", aspect_ratio=None, key="c1")
        if st.button("샘플 1 확정", key="b1"):
            arr1 = np.array(cropped1.convert("L"), dtype=np.float64)
            st.session_state.I1 = float(np.mean(arr1))
            st.success(f"I₁ = {st.session_state.I1:.2f}")
    if st.session_state.I1 is not None:
        st.info(f"✅ I₁ = {st.session_state.I1:.2f}")

# ----- 샘플 2 -----
with col2:
    st.subheader("Step 2: 순수 샘플 2")
    file2 = st.file_uploader("샘플 2 이미지", type=["png","jpg","jpeg","bmp","tif","tiff"], key="f2")
    if file2:
        img2 = Image.open(file2).convert("L")
        st.write("ROI를 드래그로 지정하세요:")
        cropped2 = st_cropper(img2.convert("RGB"), realtime_update=True,
                              box_color="#FF0000", aspect_ratio=None, key="c2")
        if st.button("샘플 2 확정", key="b2"):
            arr2 = np.array(cropped2.convert("L"), dtype=np.float64)
            st.session_state.I2 = float(np.mean(arr2))
            st.success(f"I₂ = {st.session_state.I2:.2f}")
    if st.session_state.I2 is not None:
        st.info(f"✅ I₂ = {st.session_state.I2:.2f}")

# ----- 혼합 이미지 -----
with col3:
    st.subheader("Step 3: 혼합 이미지")
    if st.session_state.I1 is None or st.session_state.I2 is None:
        st.warning("⚠️ 먼저 샘플 1과 샘플 2를 확정해주세요.")
    else:
        file3 = st.file_uploader("혼합 이미지", type=["png","jpg","jpeg","bmp","tif","tiff"], key="f3")
        if file3:
            img3 = Image.open(file3).convert("L")
            st.write("ROI를 드래그로 지정하세요:")
            cropped3 = st_cropper(img3.convert("RGB"), realtime_update=True,
                                  box_color="#00FF00", aspect_ratio=None, key="c3")
            if st.button("MI 계산", key="b3"):
                arr3 = np.array(cropped3.convert("L"), dtype=np.float64)
                result = compute_mi(arr3, st.session_state.I1, st.session_state.I2)
                if result:
                    mi, sigma, c_mean, sigma_max = result
                    st.session_state.results.append({
                        "Filename": file3.name,
                        "MI": round(mi, 4),
                        "Sigma": round(sigma, 4),
                        "Sigma_max": round(sigma_max, 4),
                        "C_mean": round(c_mean, 3),
                        "I1": round(st.session_state.I1, 2),
                        "I2": round(st.session_state.I2, 2)
                    })
                    st.success(f"🎯 MI = {mi:.4f}  ({mi*100:.1f}%)")
                    st.write(f"σ = {sigma:.4f}, σ_max = {sigma_max:.4f}, c̄ = {c_mean:.3f}")

# ===== 결과 표시 =====
st.markdown("---")
st.subheader("📊 분석 결과")
if st.session_state.results:
    df = pd.DataFrame(st.session_state.results)
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button("📥 CSV 다운로드", csv, "MI_results.csv", "text/csv")
else:
    st.info("아직 분석 결과가 없습니다.")

# ===== 푸터 =====
st.markdown("---")
st.markdown(
    f"<p style='text-align:center;color:gray;font-size:12px;'>"
    f"© {YEAR} {DEVELOPER_NAME}, {AFFILIATION}</p>",
    unsafe_allow_html=True
)
