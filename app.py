import streamlit as st
import easyocr
import json
import numpy as np
from PIL import Image
from openai import OpenAI
import os

# Load OpenAI API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or "YOUR_OPENAI_API_KEY")

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
    kb_context = "\n".join([f"{kb['keyword']}: {kb['article']}" for kb in relevant_kb]) or "No relevant KB found."

    # AI Reasoning
    with st.spinner("🤖 Analyzing error and generating resolution guide..."):
        prompt = f"""
        You are an ONTAP troubleshooting assistant.
        The following error/log was extracted: {extracted_text}
        Based on the KB data below, provide a clear, step-by-step resolution guide with CLI commands if applicable.
        KB Data:
        {kb_context}
        """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

    st.subheader("🛠 AI-Generated Resolution Guide")
    st.write(response.choices[0].message.content)
