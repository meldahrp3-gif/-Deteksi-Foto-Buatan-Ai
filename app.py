import streamlit as st
from PIL import Image
from transformers import pipeline
import base64

# ===== Fungsi Tambah Background =====
def add_bg_with_overlay(image_file):
    with open(image_file, "rb") as file:
        data = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)),
            url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
        padding-bottom: 50px;
    }}

    h1, p {{
        color: #fff !important;
        text-shadow: 0 0 6px rgba(0,0,0,0.6);
    }}

    .stFileUploader {{
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(8px);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
    }}

    button {{
        background-color: #1e1e1e !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1rem !important;
        border: none !important;
    }}
    button:hover {{
        background-color: #000 !important;
    }}

    .image-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
        width: 100%;
    }}
    .image-container img {{
        max-width: 90vw;
        height: auto;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
        object-fit: contain;
    }}

    .caption {{
        text-align: center;
        color: #ffffff;
        font-size: 14px;
        font-weight: 600;
        margin-top: 6px;
    }}

    @media (max-width: 600px) {{
        h1 {{ font-size: 22px; }}
        p {{ font-size: 14px; }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ===== Background =====
add_bg_with_overlay("bg.jpg")

# ===== Judul =====
st.markdown(
    "<h1 style='text-align:center;'>🧠 Deteksi Gambar Buatan AI</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;'>Upload gambar di bawah ini untuk mendeteksi apakah gambar tersebut buatan AI atau asli.</p>",
    unsafe_allow_html=True
)

# ===== Inisialisasi session_state =====
if "image" not in st.session_state:
    st.session_state.image = None
if "result" not in st.session_state:
    st.session_state.result = None

# ===== Upload Gambar =====
uploaded_file = st.file_uploader("📁 Pilih gambar...", type=["jpg", "jpeg", "png"])

# Jika user upload gambar baru
if uploaded_file is not None:
    st.session_state.image = Image.open(uploaded_file).convert("RGB")
    st.session_state.result = None  # reset hasil deteksi

# Jika sudah ada gambar tersimpan
if st.session_state.image is not None:
    image = st.session_state.image

    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(image, caption=None, use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<p class="caption">🖼️ Gambar yang diupload</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        detect_btn = st.button("🔍 Deteksi Gambar", use_container_width=True)
    with col2:
        clear_btn = st.button("❌ Hapus Gambar", use_container_width=True)

    # Tombol hapus: reset state & refresh halaman
    if clear_btn:
        st.session_state.image = None
        st.session_state.result = None
        st.rerun()

    # Tombol deteksi
    if detect_btn:
        with st.spinner("⏳ Mendeteksi gambar... harap tunggu..."):
            try:
                classifier = pipeline(
                    "image-classification",
                    model="NYUAD-ComNets/NYUAD_AI-generated_images_detector"
                )
                st.session_state.result = classifier(image)
            except Exception as e:
                st.error("❌ Gagal memuat model. Coba refresh halaman.")
                st.stop()

# Tampilkan hasil kalau sudah ada
if st.session_state.result:
    st.subheader("📊 Hasil Deteksi:")
    for r in st.session_state.result:
        st.write(f"**{r['label'].upper()}** : {r['score']*100:.2f}%")

    best = max(st.session_state.result, key=lambda x: x["score"])
    st.success(
        f"💡 Kesimpulan: Gambar ini kemungkinan **{best['label'].upper()}** "
        f"dengan keyakinan {best['score']*100:.2f}%"
    )

elif st.session_state.image is None:
    st.info("⬆️ Silakan upload gambar terlebih dahulu untuk dianalisis.")
