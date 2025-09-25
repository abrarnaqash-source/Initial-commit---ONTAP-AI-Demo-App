import streamlit as st
import easyocr
import json
import numpy as np
from PIL import Image

# Load mock KB dataset
with open("mock_kb.json", "r") as f:
    kb_data = json.load(f)

# OCR Reader
reader = easyocr.Reader(['en'])

# Streamlit UI
st.set_page_config(page_title="GenAI ONTAP Support Assistant", page_icon="🤖", layout="wide")
st.title("🚀 GenAI-Powered ONTAP Support Assistant")
st.write("Upload an ONTAP CLI/GUI screenshot and get an instant step-by-step resolution guide.")

uploaded_file = st.file_uploader("📤 Upload ONTAP Screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Screenshot", use_column_width=True)

    # OCR extraction
    result = reader.readtext(np.array(image), detail=0)
    extracted_text = " ".join(result)
    st.subheader("📄 Extracted Text")
    st.code(extracted_text)

    # KB Search
    relevant_kb = [kb for kb in kb_data if kb["keyword"].lower() in extracted_text.lower()]

    if relevant_kb:
        st.subheader("🛠 Resolution Guide (Mock AI)")
        for kb in relevant_kb:
            st.write(f"**Issue:** {kb['keyword']}")
            st.write(f"**Resolution:** {kb['article']}")
    else:
        st.warning("No matching KB entry found for this error.")
