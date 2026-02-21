import streamlit as st
import openai
import requests
import os
from edge_tts import Communicate
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip
import random

# =========================================================
# KONFIGURASI API (SUDAH OTOMATIS)
# =========================================================
OPENAI_API_KEY = "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"
PEXELS_API_KEY = "1MfncNTQhyT9hbvYd0l2DKQYMBp59V8CUevjAYn3j9raXx3j714KVpMs"

openai.api_key = OPENAI_API_KEY

st.set_page_config(page_title="Reddit Story Generator", layout="centered")
st.title("🎬 Reddit Story Generator")
st.write("Buat video viral TikTok/Reels otomatis!")

# Input Topik
topic = st.text_area("Masukkan topik atau awal cerita:", placeholder="Misal: Cerita horor di hutan pinus...")

def get_pexels_video(query):
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=portrait"
    r = requests.get(url, headers=headers)
    data = r.json()
    if data['videos']:
        return data['videos'][0]['video_files'][0]['link']
    return None

async def generate_voice(text):
    communicate = Communicate(text, "id-ID-ArdiNeural")
    await communicate.save("audio.mp3")

if st.button("🚀 Generate Video"):
    if not topic:
        st.error("Isi topiknya dulu dong!")
    else:
        with st.spinner("Sedang memproses..."):
            try:
                # 1. Generate Story pakai OpenAI
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": f"Buatkan cerita pendek Reddit yang menarik dalam bahasa Indonesia tentang: {topic}. Maksimal 50 kata."}]
                )
                story = response.choices[0].message.content
                st.info(f"Cerita: {story}")

                # 2. Generate Voice
                asyncio.run(generate_voice(story))

                # 3. Ambil Video Background (Parkour/Minecraft)
                video_url = get_pexels_video("parkour")
                if video_url:
                    with open("bg_video.mp4", "wb") as f:
                        f.write(requests.get(video_url).content)
                
                # 4. Editing Video (MoviePy)
                audio = AudioFileClip("audio.mp3")
                # Ambil durasi video sesuai audio, potong jika kepanjangan
                video = VideoFileClip("bg_video.mp4").subclip(0, audio.duration).resize(height=1280)
                video = video.set_audio(audio)

                # Tambahkan Teks Tengah
                txt_clip = TextClip(story, fontsize=40, color='white', font='Arial-Bold', 
                                   method='caption', size=(video.w*0.8, None)).set_duration(audio.duration).set_position('center')
                
                final_video = CompositeVideoClip([video, txt_clip])
                final_video.write_videofile("final_output.mp4", fps=24, codec="libx264")

                st.video("final_output.mp4")
                st.success("Video Berhasil Dibuat!")
                
            except Exception as e:
                st.error(f"Aduh, ada masalah: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Status: **API Ready ✅**")
st.sidebar.write("Dibuat dengan ❤️ untuk Tablet kamu")
