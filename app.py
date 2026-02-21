import streamlit as st
import google.generativeai as genai

# Penanda Versi (Ganti ini setiap kali update supaya kamu tahu kodenya berubah)
VERSION = "VERSI_TERBARU_SUBTITLE_PERKATA"

st.title(f"🎬 Video Generator ({VERSION})")

# 1. TEST KONEKSI GEMINI DULU
GEMINI_API_KEY = "AIzaSyCCaofacxUGUV_yDvIlpT_yTDXiuoV2Qn8"
genai.configure(api_key=GEMINI_API_KEY)

st.subheader("Step 1: Cek Koneksi AI")
if st.button("Test Koneksi Gemini"):
    try:
        # Kita pakai cara panggil yang paling dasar buat ngetes library
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Halo")
        st.success(f"Koneksi Berhasil! Gemini bilang: {response.text}")
    except Exception as e:
        st.error(f"Koneksi Gagal. Error: {e}")
        st.info("Kalau errornya 404, berarti Streamlit belum update library google-generativeai. Kamu HARUS Delete App dan Deploy ulang.")

# 2. LOGIKA VIDEO (Hanya muncul kalau kamu mau)
# ... (Sisanya kode yang kemarin, tapi pastikan Test di atas berhasil dulu)
