import streamlit as st
import google.generativeai as genai
import requests
import os
from edge_tts import Communicate
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

# KUNCI RAHASIA
GEMINI_API_KEY = "AIzaSyCCaofacxUGUV_yDvIlpT_yTDXiuoV2Qn8"
PEXELS_API_KEY = "1MfncNTQhyT9hbvYd0l2DKQYMBp59V8CUevjAYn3j9raXx3j714KVpMs"

genai.configure(api_key=GEMINI_API_KEY)

# JURUS ANTI ERROR 404: Mencoba mencari model yang aktif
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')

st.title("🎬 Viral One-Word Subtitle")

topic = st.text_input("Topik Cerita:")

def get_video(query):
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=portrait"
    r = requests.get(url, headers=headers)
    return r.json()['videos'][0]['video_files'][0]['link']

async def make_voice(text):
    cmt = Communicate(text, "en-US-ChristopherNeural")
    await cmt.save("suara.mp3")

if st.button("🚀 Buat Video Sekarang"):
    if topic:
        with st.spinner("Proses ini memakan waktu 5-10 menit karena subtitle per kata..."):
            try:
                # 1. Cerita (Dibuat panjang agar durasi 2 menit)
                prompt = f"Write a long, viral Reddit story about {topic}. Around 250 words, English."
                res = model.generate_content(prompt)
                cerita = res.text
                st.info("Cerita Oke!")

                # 2. Suara
                asyncio.run(make_voice(cerita))
                audio = AudioFileClip("suara.mp3")

                # 3. Background (Minecraft Parkour)
                link = get_video("minecraft parkour")
                with open("bg.mp4", "wb") as f:
                    f.write(requests.get(link).content)

                # 4. Editing Full Screen
                video_awal = VideoFileClip("bg.mp4")
                video = video_awal.loop(duration=audio.duration).resize(height=1280).set_audio(audio)

                # 5. SUBTITLE PER KATA
                words = cerita.split()
                duration_per_word = audio.duration / len(words)
                clips = [video]
                
                curr = 0
                for word in words:
                    # Teks kuning, huruf besar, di tengah (Center)
                    txt = TextClip(word.upper(), fontsize=80, color='yellow', font='Arial-Bold',
                                   stroke_color='black', stroke_width=2).set_start(curr).set_duration(duration_per_word).set_position('center')
                    clips.append(txt)
                    curr += duration_per_word

                final = CompositeVideoClip(clips)
                final.write_videofile("hasil.mp4", fps=24, codec="libx264")
                st.video("hasil.mp4")
                
            except Exception as e:
                st.error(f"Waduh: {e}")
