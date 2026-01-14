# app.py
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from qr_detector import detect_qr

# -----------------------------
# Modern UI styling (CSS)
# -----------------------------
st.set_page_config(page_title="QR Code Detector", page_icon="🔎", layout="centered")

st.markdown(
    """
    <style>
    /* ---------- Base + background ---------- */
    .stApp {
        background: radial-gradient(1200px circle at 10% 10%, rgba(99, 102, 241, 0.20), transparent 40%),
                    radial-gradient(1000px circle at 90% 20%, rgba(16, 185, 129, 0.18), transparent 45%),
                    radial-gradient(900px circle at 50% 90%, rgba(236, 72, 153, 0.12), transparent 50%),
                    linear-gradient(180deg, #0b1220 0%, #0b1220 100%);
        color: #e5e7eb;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, "Noto Sans", "Liberation Sans", sans-serif;
    }

    /* Center the main content width */
    section.main > div {
        max-width: 980px !important;
        padding-top: 2.2rem;
        padding-bottom: 2rem;
    }

    /* ---------- Card container ---------- */
    .app-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.10);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.45);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 18px;
        padding: 22px 22px 14px 22px;
        margin-top: 16px;
    }

    .muted {
        color: rgba(229, 231, 235, 0.75);
        font-size: 0.95rem;
        line-height: 1.45;
        margin-top: -6px;
    }

    /* ---------- Headings ---------- */
    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    /* ---------- File uploader ---------- */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px dashed rgba(255, 255, 255, 0.20);
        border-radius: 16px;
        padding: 16px;
        transition: all 0.2s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(99, 102, 241, 0.55);
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.12);
    }
    [data-testid="stFileUploader"] * {
        color: rgba(229, 231, 235, 0.90) !important;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        border: 0;
        border-radius: 12px;
        padding: 0.7rem 1.0rem;
        font-weight: 600;
        color: #0b1220;
        background: linear-gradient(135deg, #6366f1 0%, #22c55e 100%);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.35);
        transition: transform 0.12s ease, box-shadow 0.12s ease, filter 0.12s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        filter: brightness(1.05);
        box-shadow: 0 16px 34px rgba(0, 0, 0, 0.45);
    }
    .stButton > button:active {
        transform: translateY(0px) scale(0.99);
    }

    /* ---------- Info / success / warning boxes ---------- */
    [data-testid="stAlert"] {
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.10);
        background: rgba(255, 255, 255, 0.06);
        color: rgba(229, 231, 235, 0.95);
    }

    /* ---------- Code blocks ---------- */
    pre {
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        background: rgba(0, 0, 0, 0.28) !important;
    }

    /* ---------- Images ---------- */
    img {
        border-radius: 16px !important;
    }

    /* Hide Streamlit default footer/menu if you want a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# UI (modern card layout)
# -----------------------------
st.markdown('<div class="app-card">', unsafe_allow_html=True)

st.title("QR Code Detector")
st.markdown(
    '<p class="muted">Upload an image to detect and decode QR codes. The output is annotated with detected boundaries.</p>',
    unsafe_allow_html=True
)

uploaded = st.file_uploader("Upload an image (PNG/JPG)", type=["png", "jpg", "jpeg"])

# Optional action button to feel more "app-like"
run = False
if uploaded is not None:
    run = st.button("Detect QR Code")

if uploaded is None:
    st.info("Tip: Use a clear QR image for the best results.")
else:
    if run:
        img = Image.open(uploaded).convert("RGB")
        img_np = np.array(img)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        annotated_bgr, texts = detect_qr(img_bgr)
        annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)

        st.divider()

        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.subheader("Detection Result")
            st.image(annotated_rgb, use_container_width=True)

        with col2:
            st.subheader("Decoded Text")
            if texts:
                for i, t in enumerate(texts, 1):
                    st.code(f"{i}. {t}")
            else:
                st.info("No QR code detected.")

st.markdown("</div>", unsafe_allow_html=True)
