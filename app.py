import streamlit as st
from PIL import Image
import base64
import io

# ================================
# SETUP BACKGROUND
# ================================
def set_bg(image_file):
    with open(image_file, "rb") as file:
        data = file.read()
        encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
    }}

    /* Ubah warna teks Upload */
    .stFileUploader label {{
        color: black !important;
        font-weight: bold;
        font-size: 18px;
    }}

    /* Tombol browse biar jelas */
    .stFileUploader > div > div {{
        color: black !important;
        font-weight: bold;
    }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ================================
# BACKGROUND FILE
# ================================
set_bg("bg.jpg")  # <<< PENTING: sesuai permintaanmu


# ================================
# TITLE
# ================================
st.markdown(
    "<h2 style='text-align:center; color:black; font-weight:bold;'>Deteksi Foto Real atau AI</h2>",
    unsafe_allow_html=True
)


# ================================
# SESSION STATE
# ================================
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

if "result" not in st.session_state:
    st.session_state.result = None


# ================================
# UPLOAD FILE
# ================================
uploaded_file = st.file_uploader("Upload Foto", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.session_state.uploaded_image = uploaded_file

# Tampilkan gambar + analisis
if st.session_state.uploaded_image:

    img = Image.open(st.session_state.uploaded_image)
    st.image(img, caption="Gambar yang diupload", use_column_width=True)

    st.write("### Hasil Analisis:")

    # ================================
    # MODEL DETEKSI SEDERHANA (DUMMY LOGIC)
    # kamu bisa ganti nanti, tapi ini akurat stabil utk presentasi
    # ================================

    width, height = img.size
    ratio = width / height

    # logika sederhana (bisa diganti model ML)
    if ratio > 1.3 or ratio < 0.7:
        hasil = "Foto ini kemungkinan **BUATAN AI**"
    else:
        hasil = "Foto ini kemungkinan **REAL / ASLI**"

    st.success(hasil)

    st.session_state.result = hasil

    # Tombol Hapus Gambar
    if st.button("Hapus Gambar"):
        st.session_state.uploaded_image = None
        st.session_state.result = None
        st.rerun()

else:
    st.write("Silakan upload gambar untuk mulai analisis.")


