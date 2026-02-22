import streamlit as st
import google.generativeai as genai
import os

# 1. FIX: Paksa ImageMagick & Library Path
os.environ["IMAGE_MAGICK_BINARY"] = "/usr/bin/convert"

# 2. SETUP API
GEMINI_API_KEY = "AIzaSyCCaofacxUGUV_yDvIlpT_yTDXiuoV2Qn8"
genai.configure(api_key=GEMINI_API_KEY)

st.title("🎬 AI Video Creator Final")

# Diagnosis Versi (Biar kita tahu kenapa 404)
st.sidebar.write(f"Library Version: {genai.__version__}")

topic = st.text_input("Topik Cerita:")

if st.button("GENERATE"):
    try:
        # Gunakan GenerativeModel dengan konfigurasi lebih ketat
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config={"speed_optimized": True}
        )
        
        # Tes panggil model
        response = model.generate_content(f"Tell a 20-word story about {topic}")
        st.success("🤖 Gemini Terkoneksi!")
        st.write(response.text)
        
    except Exception as e:
        st.error(f"Waduh, masih error: {e}")
        st.info("Kalau muncul 404, artinya library google-generativeai di server kamu masih versi KUNO.")
