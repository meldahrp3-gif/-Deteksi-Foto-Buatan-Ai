import streamlit as st
from transformers import pipeline
from PIL import Image

# --- Konfigurasi halaman ---
st.set_page_config(
    page_title="Deteksi Gambar Buatan AI",
    page_icon="🧠",
    layout="centered",
)

# --- CSS untuk tampilan keren ---
st.markdown("""
    <style>
    body {
        background-image: url('https://images.unsplash.com/photo-1534751516642-a1af1ef26a56?auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white;
    }
    .title {
        text-align: center;
        font-weight: 800;
        font-size: 38px;
        color: white;
        text-shadow: 2px 2px 8px #00000080;
    }
    .subtitle {
        text-align: center;
        color: #e5e5e5;
        font-size: 16px;
        margin-top: -10px;
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
    }
    .stButton>button:hover {
        background-color: #ff6b6b;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- Judul utama ---
st.markdown('<h1 class="title">🧠 Deteksi Gambar Buatan AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload gambar untuk memeriksa apakah itu buatan AI atau asli.</p>', unsafe_allow_html=True)

# --- Load model deteksi ---
@st.cache_resource
def load_model():
    return pipeline("image-classification", model="umm-maybe/AI-image-detector")

detector = load_model()

# --- Upload gambar ---
uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    # tampilkan gambar dengan ukuran lebih kecil (biar pas di HP)
    st.image(image, caption="🖼️ Gambar yang diupload", use_column_width=True)

    # tombol deteksi
    if st.button("🔍 Deteksi Gambar"):
        with st.spinner("Menganalisis gambar..."):
            result = detector(image)

            # ambil hasil terbaik
            best = max(result, key=lambda x: x['score'])
            label = best['label'].lower()
            score = best['score']

            # threshold biar gak gampang salah
            if score > 0.65:
                if "ai" in label or "fake" in label:
                    st.error(f"🚨 Gambar ini kemungkinan **BUATAN AI** ({score*100:.2f}%)")
                else:
                    st.success(f"✅ Gambar ini kemungkinan **ASLI / REAL** ({score*100:.2f}%)")
            else:
                st.warning("⚠️ Hasil tidak meyakinkan — coba gambar lain atau kualitas lebih tinggi.")

        st.info("💡 Tips: Gunakan gambar dengan wajah/judul jelas agar hasil lebih akurat.")

else:
    st.write("📸 Silakan upload gambar terlebih dahulu.")

# --- Footer ---
st.markdown("""
    <hr style="border: 0.5px solid rgba(255,255,255,0.2);">
    <p style="text-align:center; font-size:13px; color:#ccc;">
    Dibuat dengan ❤️ oleh Melda | Versi Akurasi Tinggi
    </p>
""", unsafe_allow_html=True)
