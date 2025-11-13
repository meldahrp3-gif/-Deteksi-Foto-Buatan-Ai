import streamlit as st
from PIL import Image
import base64
import random

# ===============================
# Konfigurasi halaman
# ===============================
st.set_page_config(
    page_title="Deteksi Gambar Buatan AI",
    layout="centered",
    page_icon="🧠"
)

# ===============================
# Fungsi untuk set background
# ===============================
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    page_bg = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    [data-testid="stHeader"], [data-testid="stToolbar"] {{
        background: rgba(0,0,0,0);
    }}
    .stApp {{
        background: rgba(0,0,0,0.5);
    }}
    .title {{
        text-align: center;
        font-size: 36px;
        color: white;
        font-weight: bold;
        text-shadow: 2px 2px 6px #000000;
    }}
    .desc {{
        text-align: center;
        color: #f0f0f0;
        font-size: 18px;
        margin-bottom: 30px;
    }}
    .stProgress > div > div {{
        background-color: #FF4B4B !important;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

# Ganti dengan nama file background kamu (pastikan file ini ada di folder project)
set_background("tzu.PNG")

# ===============================
# Judul & Deskripsi
# ===============================
st.markdown("<h1 class='title'>🧠 Deteksi Gambar Buatan AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='desc'>Upload gambar di bawah ini untuk mendeteksi apakah gambar tersebut buatan AI atau asli.</p>", unsafe_allow_html=True)

# ===============================
# Upload gambar
# ===============================
uploaded_file = st.file_uploader("📁 Pilih gambar...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="🖼️ Gambar yang diunggah", use_container_width=True)

    # Simulasi hasil deteksi (nanti bisa diganti model sebenarnya)
    dalle_score = round(random.uniform(0, 100), 2)
    sd_score = round(random.uniform(0, 100), 2)
    real_score = round(random.uniform(0, 100), 2)

    results = {
        "DALLE": dalle_score,
        "Stable Diffusion": sd_score,
        "Real / Asli": real_score
    }

    st.markdown("<h3 style='color:white;margin-top:25px;'>📊 Hasil Deteksi:</h3>", unsafe_allow_html=True)
    for model, score in results.items():
        st.markdown(f"<b style='color:white;'>{model}</b>", unsafe_allow_html=True)
        st.progress(int(score))
        st.markdown(f"<span style='color:#f0f0f0;'>{score}%</span>", unsafe_allow_html=True)

    # Hasil tertinggi
    final_label = max(results, key=results.get)
    confidence = results[final_label]

    st.markdown("---")
    st.markdown(
        f"<h3 style='color:#00FFAA;text-align:center;'>🧩 Gambar ini kemungkinan besar "
        f"<span style='color:#FFD700;'>{final_label}</span> "
        f"dengan tingkat keyakinan {confidence}%.</h3>",
        unsafe_allow_html=True
    )

else:
    st.info("📸 Silakan upload gambar terlebih dahulu.")

# ===============================
# Catatan
# ===============================
st.markdown(
    "<p style='color:#d0d0d0; font-size:14px; text-align:center;'>© 2025 Deteksi Foto AI - Dibuat oleh Melda 💖</p>",
    unsafe_allow_html=True
)
