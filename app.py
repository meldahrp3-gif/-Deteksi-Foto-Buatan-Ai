# app.py (paste ke repo, replace existing)
import streamlit as st
from PIL import Image
from transformers import pipeline
import base64

# -------------------------
# Utility: background css
# -------------------------
def add_bg_with_overlay(image_file="bg.jpg"):
    try:
        with open(image_file, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
                url("data:image/png;base64,{data}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }}
        .stFileUploader {{
            background: rgba(255,255,255,0.92);
            border-radius: 12px;
            padding: 8px;
            text-align: center;
        }}
        .image-container img {{
            max-width: 90vw;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
        }}
        button {{ padding: 0.5rem 0.8rem !important; border-radius: 8px !important; }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except FileNotFoundError:
        # jika bg.jpg tidak ada, skip
        pass

add_bg_with_overlay()

st.markdown("<h1 style='text-align:center;'>🧠 Deteksi Gambar Buatan AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload gambar untuk mendeteksi apakah gambar dibuat AI atau bukan.</p>", unsafe_allow_html=True)

# -------------------------
# Session state init
# -------------------------
if "image" not in st.session_state:
    st.session_state.image = None
if "result" not in st.session_state:
    st.session_state.result = None
if "uploader_cleared" not in st.session_state:
    st.session_state.uploader_cleared = False

# -------------------------
# Cached model loader (load once)
# -------------------------
@st.cache_resource
def get_classifier():
    # pakai pipeline — cached agar tidak load berulang
    try:
        clf = pipeline(
            "image-classification",
            model="NYUAD-ComNets/NYUAD_AI-generated_images_detector"
        )
    except Exception as e:
        # kembalikan exception supaya caller tahu
        raise e
    return clf

# -------------------------
# File uploader (with key)
# -------------------------
uploaded = st.file_uploader("📁 Pilih gambar...", type=["jpg", "jpeg", "png"], key="uploader")

# Jika ada upload baru, simpan ke session_state.image
if uploaded is not None:
    try:
        st.session_state.image = Image.open(uploaded).convert("RGB")
        st.session_state.result = None
        st.session_state.uploader_cleared = False
    except Exception as e:
        st.error("File tidak valid. Coba pakai JPG/PNG.")
        st.session_state.image = None

# -------------------------
# Jika ada gambar: tampilkan + tombol
# -------------------------
if st.session_state.image is not None:
    image = st.session_state.image
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(image, use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # dua tombol responsif
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("🔍 Deteksi Gambar", key="detect_btn"):
            # deteksi
            with st.spinner("⏳ Mendeteksi..."):
                try:
                    classifier = get_classifier()
                except Exception as e:
                    st.error("Gagal memuat model deteksi. Pesan error: " + str(e))
                    st.stop()

                try:
                    res = classifier(image)
                    st.session_state.result = res
                except Exception as e:
                    st.error("Error saat inferensi: " + str(e))
                    st.session_state.result = None

    with col2:
        if st.button("❌ Hapus Gambar", key="clear_btn"):
            # Reset uploader + session state
            # Cara yang aman: set nilai key uploader ke None lalu rerun
            try:
                st.session_state.uploader = None   # reset widget state
            except Exception:
                pass
            st.session_state.image = None
            st.session_state.result = None
            st.session_state.uploader_cleared = True
            st.experimental_rerun()

# -------------------------
# Tampilkan hasil bila ada
# -------------------------
if st.session_state.result:
    st.subheader("📊 Hasil Deteksi:")
    for r in st.session_state.result:
        st.write(f"**{r['label'].upper()}** : {r['score']*100:.2f}%")
    best = max(st.session_state.result, key=lambda x: x["score"])
    st.success(f"💡 Kesimpulan: Gambar ini kemungkinan **{best['label'].upper()}** dengan keyakinan {best['score']*100:.2f}%")

# Jika kosong
elif st.session_state.image is None:
    st.info("⬆️ Silakan upload gambar terlebih dahulu untuk dianalisis.")
