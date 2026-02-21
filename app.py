import streamlit as st
import os
import sys

st.set_page_config(page_title="Debugger Mode", icon="🔍")
st.title("🔍 Deep Debugger: Mencari Jejak DB_USERNAME")

# --- TEST 1: SCAN ISI FILE ---
st.subheader("1. File Scan (Mencari Teks Tersembunyi)")
try:
    with open(__file__, "r") as f:
        lines = f.readlines()
        found = False
        for i, line in enumerate(lines):
            if "DB_USERNAME" in line:
                st.error(f"🚨 BARIS {i+1}: Ditemukan teks 'DB_USERNAME'!")
                st.code(line.strip())
                found = True
        if not found:
            st.success("✅ Tidak ada teks 'DB_USERNAME' di dalam file ini.")
except Exception as e:
    st.error(f"Gagal membaca file: {e}")

# --- TEST 2: KONEKSI GEMINI (PENYEBAB 404) ---
st.subheader("2. Diagnostic Library & AI")
try:
    import google.generativeai as genai
    v = genai.__version__
    st.write(f"Versi Google AI: `{v}`")
    
    # Cek apakah model flash tersedia di versi ini
    GEMINI_API_KEY = "AIzaSyCCaofacxUGUV_yDvIlpT_yTDXiuoV2Qn8" # Pakai key kamu
    genai.configure(api_key=GEMINI_API_KEY)
    
    models = [m.name for m in genai.list_models()]
    st.write("Model yang tersedia:")
    st.json(models)
    
    if 'models/gemini-1.5-flash' in models:
        st.success("✅ Model Flash TERSEDIA!")
    else:
        st.warning("⚠️ Model Flash TIDAK ditemukan di list.")
except Exception as e:
    st.error(f"❌ Error saat cek AI: {e}")

# --- TEST 3: STREAMLIT SECRETS ---
st.subheader("3. Streamlit Secrets & Environment")
if st.secrets:
    st.write("Daftar kunci di Secrets:")
    st.json(list(st.secrets.keys()))
    if "DB_USERNAME" in st.secrets:
        st.error("🚨 KETEMU! DB_USERNAME ada di bagian SECRETS Streamlit Cloud kamu.")
else:
    st.write("Secrets kosong.")

# --- TEST 4: CHECK PATH ---
st.subheader("4. System Path")
st.write(f"Python executable: `{sys.executable}`")
st.write(f"Current Directory: `{os.getcwd()}`")
