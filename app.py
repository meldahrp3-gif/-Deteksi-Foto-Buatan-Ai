import streamlit as st
from PIL import Image
from transformers import pipeline
import base64

# ===========================
# FUNGSI BACKGROUND
# ===========================
def add_bg(image_file):
    with open(image_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    css = f"""
    <style>

    /* Background */
    .stApp {{
        background-image:
            linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
            url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Judul & teks */
    h1, p {{
        color: white !important;
        text-shadow: 0 0 8px rgba(0,0,0,0.8);
    }}

    /* Box Upload */
    .stFileUploader {{
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0,0,0,0.4);
        color: black !important;
    }}

    /* Tulisan "Pilih gambar" */
    label {{
        color: black !important;
        font-weight: 700 !important;
    }}

    /* Browse Files button */
    .stFileUploader button {{
        background-color: black !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 6px 18px !important;
    }}

    .stFileUploader button:hover {{
        background-color: #333 !important;
    }}

    /* Tombol deteksi & hapus */
    button {{
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.6rem 1rem !important;
        font-size: 16px !important;
    }}

    .btn-detect {{
        background-color: #ffffff !important;
        color: black !important;
    }}
    .btn-detect:hover {{
        background-color: #e6e6e6 !important;
    }}

    .btn-clear {{
        background-color: #cc0000 !important;
        color: white !important;
    }}
    .btn-clear:hover {{
        background-color: #a50000 !important;
    }}

    /* Gambar */
    .image-container img {{
        max-width: 90%;
        border-radius: 14px;
        box-shadow: 0 0 12px rgba(0,0,0,0.6);
    }}

    .caption {{
        color: white;
        font-size: 14px;
        text-align: center;
        margin-top: 5px;
        font-weight: bold;
    }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# 🔥 Terapkan Background
add_bg("bg.jpg")

# ===========================
# JUDUL
# ===========================
st.markdown("<h1 style='text-align:center;'>🧠 Deteksi Gambar Buatan AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload gambar untuk mengetahui apakah ini REAL atau buatan AI (DALLE).</p>", unsafe_allow_html=True)

# ===========================
# SESSION STATE
# ===========================
if "img" not in st.session_state:
    st.session_state.img = None
if "result" not in st.session_state:
    st.session_state.result = None

# ===========================
# UPLOAD GAMBAR
# ===========================
uploaded = st.file_uploader("Pilih gambar...", type=["jpg","jpeg","png"])

if uploaded:
    st.session_state.img = Image.open(uploaded).convert("RGB")
    st.session_state.result = None

# ===========================
# TAMPILKAN GAMBAR
# ===========================
if st.session_state.img:
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(st.session_state.img, use_column_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<p class='caption'>📷 Gambar yang di-upload</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        detect_btn = st.button("🔍 Deteksi Gambar", type="primary", use_container_width=True, key="detect", help="", on_click=None)
    with col2:
        clear_btn = st.button("🗑️ Hapus Gambar", use_container_width=True, key="clear")

    # Tombol hapus berfungsi
    if clear_btn:
        st.session_state.img = None
        st.session_state.result = None
        st.rerun()

    # Tombol deteksi
    if detect_btn:
        with st.spinner("Mendeteksi gambar..."):
            classifier = pipeline(
                "image-classification",
                model="NYUAD-ComNets/NYUAD_AI-generated_images_detector"
            )
            st.session_state.result = classifier(st.session_state.img)

# ===========================
# HASIL DETEKSI
# ===========================
if st.session_state.result:
    st.subheader("📊 Hasil Deteksi:")

    label_map = {"ai_generated": "DALLE (AI)", "real": "REAL"}
    final = {}

    for r in st.session_state.result:
        label = label_map.get(r["label"], r["label"])
        final[label] = r["score"] * 100

    for key, val in final.items():
        st.write(f"**{key}** : {val:.2f}%")

    best = max(final, key=final.get)
    st.success(f"💡 Gambar ini kemungkinan **{best}** dengan keyakinan **{final[best]:.2f}%**")

elif st.session_state.img is None:
    st.info("⬆️ Silakan upload gambar terlebih dahulu.")
