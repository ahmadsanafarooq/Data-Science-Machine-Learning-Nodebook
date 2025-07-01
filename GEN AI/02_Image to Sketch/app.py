import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
from io import BytesIO

st.set_page_config(page_title="Sketchify Image Pro", layout="centered")
st.title("🖼️ Advanced Image to HD Sketch Converter")

uploaded_file = st.file_uploader("📷 Upload an image", type=["jpg", "jpeg", "png"])

# Function to convert image to HD sketch
def sketch_image(img: Image.Image, blur_strength: int, contrast: float):
    img_rgb = np.array(img)
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (blur_strength, blur_strength), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    sketch_pil = Image.fromarray(sketch)
    sketch_pil = ImageEnhance.Contrast(sketch_pil).enhance(contrast)
    return sketch_pil

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="🖼️ Original Image", use_column_width=True)

    st.sidebar.header("🎛️ Customize Sketch")
    blur_strength = st.sidebar.slider("Blur Strength", min_value=5, max_value=51, value=21, step=2)
    contrast = st.sidebar.slider("Contrast Level", min_value=0.5, max_value=3.0, value=1.5, step=0.1)

    with st.spinner("🎨 Creating enhanced sketch..."):
        result = sketch_image(image, blur_strength, contrast)

    st.image(result, caption="📝 HD Enhanced Sketch", use_column_width=True)

    # Download sketch
    buf = BytesIO()
    result.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button("📥 Download Sketch", data=byte_im, file_name="sketch.png", mime="image/png")
else:
    st.info("Upload an image to get started.")
