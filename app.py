import streamlit as st
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
import base64

# ===== Fungsi Background dengan Overlay =====
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
    .stFileUploader label, 
    .stFileUploader p,
    .stFileUploader div {{
        color: #000000 !important;
        font-weight: 600;
        text-shadow: none !important;
    }}
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
st.markdown("<h1 style='text-align:center;'>🧠 Deteksi Gambar Buatan AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload gambar di bawah ini untuk mendeteksi apakah gambar tersebut buatan AI atau asli.</p>", unsafe_allow_html=True)

# ===== Upload Gambar =====
uploaded_file = st.file_uploader("📁 Pilih gambar...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(image, caption=None, use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<p class="caption">🖼️ Gambar yang diupload</p>', unsafe_allow_html=True)

    with st.spinner("🔍 Mendeteksi gambar... harap tunggu..."):
        # Load model Hugging Face
        processor = AutoImageProcessor.from_pretrained("NYUAD-ComNets/NYUAD_AI-generated_images_detector")
        model = AutoModelForImageClassification.from_pretrained("NYUAD-ComNets/NYUAD_AI-generated_images_detector")

        # Preprocessing & inference
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1)
            results = [
                {"label": model.config.id2label[i], "score": float(probs[0][i])}
                for i in range(len(model.config.id2label))
            ]

    st.subheader("📊 Hasil Deteksi:")
    for r in results:
        st.write(f"**{r['label'].upper()}** : {r['score']*100:.2f}%")

    best = max(results, key=lambda x: x["score"])
    st.success(
        f"💡 Kesimpulan: Gambar ini kemungkinan **{best['label'].upper()}** "
        f"dengan keyakinan {best['score']*100:.2f}%"
    )
