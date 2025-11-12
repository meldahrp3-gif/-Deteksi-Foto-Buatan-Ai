import streamlit as st
from PIL import Image
from transformers import pipeline
import base64

# ===== Fungsi Tambah Background dengan Overlay =====
def add_bg_with_overlay(image_file):
    with open(image_file, "rb") as file:
        data = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0.55)),
            url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}

    h1, h2, h3, h4, h5, h6, p, label, span {{
        color: #ffffff !important;
        text-shadow: 0 0 8px rgba(0,0,0,0.7);
    }}

    .stFileUploader {{
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(8px);
        border: 2px solid rgba(0,0,0,0.3);
        border-radius: 15px;
        padding: 1.2rem;
        text-align: center;
    }}

    /* Tulisan dalam uploader tetap hitam */
    .stFileUploader label, 
    .stFileUploader p,
    .stFileUploader div {{
        color: #000000 !important;
        font-weight: 600;
        text-shadow: none !important;
    }}

    /* Tombol browse */
    button[kind="secondary"] {{
        background-color: rgba(0,0,0,0.85) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        border: none !important;
    }}
    button[kind="secondary"]:hover {{
        background-color: rgba(0,0,0,1) !important;
    }}

    .image-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
    }}
    .image-container img {{
        width: 200px;
        height: auto;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.6);
        object-fit: contain;
    }}

    .caption {{
        text-align: center;
        color: #ffffff;
        font-size: 14px;
        font-weight: 600;
        margin-top: 6px;
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

# ===== Upload Gambar =====
uploaded_file = st.file_uploader("📁 Pilih gambar...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    # Tampilkan gambar
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(image, caption=None, use_column_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<p class="caption">🖼️ Gambar yang diupload</p>', unsafe_allow_html=True)

    # ===== Proses Deteksi =====
    with st.spinner("🔍 Mendeteksi gambar... harap tunggu..."):
        try:
            classifier = pipeline(
                "image-classification",
                model="NYUAD-ComNets/NYUAD_AI-generated_images_detector"
            )
            result = classifier(image)
        except Exception as e:
            st.error("Gagal memuat model. Coba refresh halaman atau cek koneksi.")
            st.stop()

    # ===== Tampilkan Hasil =====
    st.subheader("📊 Hasil Deteksi:")
    for r in result:
        st.write(f"**{r['label'].upper()}** : {r['score']*100:.2f}%")

    best = max(result, key=lambda x: x["score"])
    st.success(
        f"💡 Kesimpulan: Gambar ini kemungkinan **{best['label'].upper()}** "
        f"dengan keyakinan {best['score']*100:.2f}%"
    )

else:
    st.info("⬆️ Silakan upload gambar terlebih dahulu untuk dianalisis.")
