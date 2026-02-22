import streamlit as st
import google.generativeai as genai
import os

# 1. FIX: Pastikan Path ImageMagick Benar
os.environ["IMAGE_MAGICK_BINARY"] = "/usr/bin/convert"

# 2. SETUP API
GEMINI_API_KEY = "AIzaSyCCaofacxUGUV_yDvIlpT_yTDXiuoV2Qn8"
genai.configure(api_key=GEMINI_API_KEY)

st.title("🎬 AI Video Creator Final")

# Sidebar untuk cek versi (Penting untuk diagnosa 404)
st.sidebar.write(f"Library Version: {genai.__version__}")

topic = st.text_input("Topik Cerita:", placeholder="Contoh: Misteri di stasiun tua")

if st.button("GENERATE STORY"):
    if topic:
        try:
            with st.spinner("🤖 Gemini sedang menulis cerita..."):
                # Panggil model tanpa config yang aneh-aneh
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Tambahkan instruksi agar cerita pendek saja
                prompt = f"Write a very short 40-word horror story about {topic}. English only."
                response = model.generate_content(prompt)
                
                st.success("✅ Gemini Berhasil Menjawab!")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Waduh, ada error: {e}")
    else:
        st.warning("Masukkan topik dulu ya!")
