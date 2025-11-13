import streamlit as st
from transformers import pipeline
from PIL import Image
import io

# --- Konfigurasi halaman ---
st.set_page_config(
    page_title="Deteksi Gambar Buatan AI",
    page_icon="🧠",
    layout="centered",
)

# --- CSS Tampilan dengan background kamu ---
st.markdown("""
    <style>
    body {
        background-image: url('bg.jpg');  /* gunakan nama background kamu */
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        color: white;
    }
    .title {
        text-align: center;
        font-weight: 800;
        font-size: 38px;
        color: white;
        text-shadow: 2px 2px 8px #00000080;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #e5e5e5;
        font-size: 16px;
        margin-bottom: 25px;
    }
    .stFileUploader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(6px);
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #ff6b6b;
        transform: scale(1.05);
    }
    .result-box {
        text-align: center;
        margin-top: 25px;
        padding: 15px;
        border-radius: 12px;
        background-color: rgba(0, 0, 0, 0.6);
    }
    .percent {
        font-size: 30px;
        font-weight: 700;
        color: #ffd700;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Judul utama ---
st.markdown('<h1 class="title">🧠 Deteksi Gambar Buatan AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload gambar di bawah ini untuk mendeteksi apakah gambar tersebut buatan AI atau asli.</p>', unsafe_allow_html=True)

# --- Muat model deteksi ---
@st.cache_resource
def load_model():
    return pipeline("image-classification", model="umm-maybe/AI-image-detector")

detector = load_model()

# --- Upload gambar ---
uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    # tampilkan gambar yang di-upload
    st.image(image, caption="🖼️ Gambar yang diupload", use_column_width=True)

    # tombol deteksi
    if st.button("🔍 Deteksi Gambar"):
        with st.spinner("Menganalisis gambar..."):
            result = detector(image)

            # ambil hasil terbaik
            best = max(result, key=lambda x: x['score'])
            label = best['label'].lower()
            score = best['score']

            # tampilkan hasil
            st.markdown('<div class="result-box">', unsafe_allow_html=True)

            if "ai" in label or "fake" in label:
                st.markdown(f"<h3>🚨 Gambar ini kemungkinan <b>BUATAN AI</b></h3>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h3>✅ Gambar ini kemungkinan <b>ASLI / REAL</b></h3>", unsafe_allow_html=True)

            st.markdown(f'<p class="percent">Akurasi: {score*100:.2f}%</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.info("💡 Tips: Gunakan gambar dengan kualitas tinggi agar hasil lebih akurat.")

else:
    st.write("📸 Silakan upload gambar terlebih dahulu.")

# --- Footer ---
st.markdown("""
    <hr style="border: 0.5px solid rgba(255,255,255,0.2); margin-top: 40px;">
    <p style="text-align:center; font-size:13px; color:#ccc;">
    Dibuat dengan ❤️ oleh Melda | Background: tzu.PNG
    </p>
""", unsafe_allow_html=True)
