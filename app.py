import streamlit as st
import google.generativeai as genai
import os
import asyncio
from edge_tts import Communicate
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip

# 1. FIX: Pastikan ImageMagick terbaca
os.environ["IMAGE_MAGICK_BINARY"] = "/usr/bin/convert"

# 2. SETUP API (Langsung di kode biar gak ribet sama Secrets)
GEMINI_API_KEY = "AIzaSyCCaofacxUGUV_yDvIlpT_yTDXiuoV2Qn8"
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="AI Video Pro", page_icon="🎬")
st.title("🎬 AI Story Video Creator")

topic = st.text_input("Topik Cerita:", placeholder="Misal: Cerita horor di sekolah")

# Fungsi Audio
async def generate_audio(text):
    communicate = Communicate(text, "en-US-ChristopherNeural")
    await communicate.save("audio.mp3")

if st.button("🚀 MULAI BUAT VIDEO"):
    if not topic:
        st.warning("Isi dulu topiknya, bos!")
    else:
        try:
            with st.spinner("🤖 Gemini lagi mikir cerita..."):
                # Gunakan cara panggil model yang lebih aman
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Write a very short 50-word horror story about {topic}. English only.")
                story_text = response.text
                st.write(f"📜 **Cerita:** {story_text}")

            with st.spinner("🎙️ Mengubah suara Christopher..."):
                asyncio.run(generate_audio(story_text))
                st.audio("audio.mp3")
                
            st.success("✅ Berhasil! Untuk video lengkapnya, pastikan ffmpeg sudah ada di packages.txt")
            
        except Exception as e:
            if "404" in str(e):
                st.error("❌ Error 404: Server Streamlit kamu pakai library Google AI versi jadul. Solusinya: Tambahkan 'google-generativeai>=0.7.2' di requirements.txt lalu Reboot.")
            else:
                st.error(f"❌ Ada masalah: {e}")
