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
    .stApp {{
        background-image:
            linear-gradient(rgba(0,0,0,0.60), rgba(0,0,0,0.60)),
            url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    h1, p {{
        color: white !important;
        text-shadow: 0 0 8px rgba(0,0,0,0.8);
    }}

    /* Upload box */
    .stFileUploader {{
        background: rgba(255,255,255,0.92);
        border-radius: 14px;
        padding: 20px;
        backdrop-filter: blur(5px);
        box-shadow: 0 0 8px rgba(0,0,0,0.4);
    }}

    .image-container img {{
        max-width: 90%;
        border-radius: 14px;
        box-shadow: 0 0 12px rgba(0,0,0,0.6);
    }}

    button {{
        background-color: #ffffff !important;
        color: black !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.6rem 1rem !important;
    }}
    button:hover {{
        background-color: #dcdcdc !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Tambahkan background (pastikan file bg.jpg ada di folder app.py)
add_bg("bg.jpg")

# ===========================
# JUDUL
# ===========================
st.markdown(
    "<h1 style='text-align:center;'>🧠 Deteksi Gambar Buatan AI</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;'>Upload gambar untuk mendeteksi apakah gambar ini REAL atau AI (DALLE).</p>",
    unsafe_allow_html=True,
)

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
uploaded = st.file_uploader("📁 Pilih Gambar...", type=["jpg","jpeg","png"])

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

    detect = st.button("🔍 Deteksi Gambar", use_container_width=True)

    if detect:
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
    st.subheader("📊 Hasil Deteksi")

    label_map = {
        "ai_generated": "DALLE (BUATAN AI)",
        "real": "REAL"
    }

    final = {}

    for r in st.session_state.result:
        label = label_map.get(r["label"], r["label"])
        final[label] = r["score"] * 100

    # tampilkan persentase
    for key, val in final.items():
        st.write(f"**{key}** : {val:.2f}%")

    # kesimpulan
    best = max(final, key=final.get)

    st.success(f"💡 Gambar ini kemungkinan **{best}** dengan keyakinan **{final[best]:.2f}%**")

else:
    st.info("⬆️ Silakan upload gambar untuk dianalisis.")
