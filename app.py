import streamlit as st
from PIL import Image
from transformers import pipeline
import base64

# ==========================================================
# Fungsi background + styling
# ==========================================================
def set_background(image_file="bg.jpg"):
    with open(image_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
            url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
        font-family: 'Poppins', sans-serif;
    }}

    h1, h2, h3, p, label {{
        color: white !important;
        text-shadow: 0 0 8px rgba(0,0,0,0.7);
    }}

    .stFileUploader {{
        background: rgba(255, 255, 255, 0.9);
        border-radius: 14px;
        padding: 1rem;
        border: 2px solid rgba(0,0,0,0.4);
        text-align: center;
    }}

    .stFileUploader label, .stFileUploader p {{
        color: black !important;
        font-weight: 600;
    }}

    .image-container {{
        display: flex;
        justify-content: center;
        margin-top: 15px;
    }}
    .image-container img {{
        width: 80%;
        max-width: 300px;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }}

    .result-box {{
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 10px 15px;
        margin-top: 15px;
        backdrop-filter: blur(6px);
    }}

    .stButton > button {{
        background-color: rgba(255,255,255,0.2);
        border: 2px solid white;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
    }}
    .stButton > button:hover {{
        background-color: rgba(255,255,255,0.35);
        border: 2px solid #f0f0f0;
        color: #000;
    }}
    </style>
    """, unsafe_allow_html=True)


# ==========================================================
# Terapkan background
# ==========================================================
set_background("bg.jpg")

# ==========================================================
# Judul
# ==========================================================
st.markdown("<h1 style='text-align:center;'>🧠 Deteksi Foto Buatan AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload gambar untuk mendeteksi apakah foto ini asli atau buatan AI.</p>", unsafe_allow_html=True)

# ==========================================================
# Cache model (agar load cepat)
# ==========================================================
@st.cache_resource
def load_model():
    return pipeline(
        "image-classification",
        model="NYUAD-ComNets/NYUAD_AI-generated_images_detector"
    )

classifier = load_model()

# ==========================================================
# Upload gambar dan langsung deteksi
# ==========================================================
uploaded = st.file_uploader("📁 Pilih gambar...", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded).convert("RGB")

    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(image, caption="📸 Gambar yang diupload", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    with st.spinner("🔍 Mendeteksi... harap tunggu..."):
        result = classifier(image)

    # tampilkan hasil
    best = max(result, key=lambda x: x["score"])
    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
    st.subheader("📊 Hasil Deteksi:")
    for r in result:
        st.write(f"**{r['label'].upper()}** : {r['score']*100:.2f}%")

    if "ai" in best["label"].lower():
        st.error(f"🚨 Gambar ini kemungkinan **BUATAN AI** ({best['score']*100:.2f}%)")
    else:
        st.success(f"✅ Gambar ini kemungkinan **ASLI / REAL** ({best['score']*100:.2f}%)")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("⬆️ Silakan upload gambar terlebih dahulu untuk dideteksi.")
