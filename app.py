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
    }}

    h1, h2, h3, h4, h5, h6, p, label, span {{
        color: #ffffff !important;
        text-shadow: 0 0 6px rgba(0,0,0,0.7);
    }}

    .stFileUploader {{
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(8px);
        border: 2px solid rgba(0,0,0,0.3);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
    }}

    button {{
        background-color: #222 !important;
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
add_bg_with_overlay("dhwi.PNG")

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

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(image, use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<p class="caption">🖼️ Gambar yang diupload</p>', unsafe_allow_html=True)

    # ===== Tombol Deteksi =====
    if st.button("🔍 Deteksi Gambar", use_container_width=True):
        with st.spinner("⏳ Mendeteksi gambar... harap tunggu..."):
            try:
                classifier = pipeline(
                    "image-classification",
                    model="umm-maybe/AI-image-detector"
                )
                result = classifier(image)
            except Exception as e:
                st.error("❌ Gagal memuat model. Silakan refresh dan coba lagi.")
                st.stop()

        # ===== Hasil hanya untuk DALLE & REAL =====
        st.subheader("📊 Hasil Deteksi:")
        filtered = [r for r in result if r['label'].upper() in ['DALLE', 'REAL']]
        if filtered:
            for r in filtered:
                st.write(f"**{r['label'].upper()}** : {r['score']*100:.2f}%")

            best = max(filtered, key=lambda x: x["score"])
            st.success(
                f"💡 Kesimpulan: Gambar ini kemungkinan **{best['label'].upper()}** "
                f"dengan keyakinan {best['score']*100:.2f}%"
            )
        e
