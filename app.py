import streamlit as st
import google.generativeai as genai
import requests
import os
from edge_tts import Communicate
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

# CONFIG
GEMINI_API_KEY = "AIzaSyCCaofacxUGUV_yDvIlpT_yTDXiuoV2Qn8"
PEXELS_API_KEY = "1MfncNTQhyT9hbvYd0l2DKQYMBp59V8CUevjAYn3j9raXx3j714KVpMs"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🎬 Viral One-Word Subtitle Creator")

topic = st.text_input("Topik Cerita (Contoh: Haunted House):")

def get_video(query):
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=portrait"
    r = requests.get(url, headers=headers)
    return r.json()['videos'][0]['video_files'][0]['link']

async def make_voice(text):
    cmt = Communicate(text, "en-US-ChristopherNeural")
    await cmt.save("suara.mp3")

if st.button("🚀 GENERATE VIDEO FINAL"):
    if not topic:
        st.error("Isi topik dulu!")
    else:
        with st.spinner("Sedang merender subtitle per kata... (Bisa 10 menit, jangan diclose!)"):
            try:
                # 1. Cerita
                res = model.generate_content(f"Write a 150 word gripping story about {topic}. English.")
                cerita = res.text
                st.info("Cerita Berhasil Dibuat!")

                # 2. Suara
                asyncio.run(make_voice(cerita))
                audio = AudioFileClip("suara.mp3")

                # 3. Video
                with open("bg.mp4", "wb") as f:
                    f.write(requests.get(get_video("minecraft parkour")).content)

                # 4. Editing
                video = VideoFileClip("bg.mp4").loop(duration=audio.duration).resize(height=1280).set_audio(audio)

                # 5. SUBTITLE PER KATA
                words = cerita.split()
                duration_per_word = audio.duration / len(words)
                clips = [video]
                curr = 0
                for word in words:
                    txt = TextClip(word.upper(), fontsize=70, color='yellow', font='Arial-Bold',
                                   stroke_color='black', stroke_width=2).set_start(curr).set_duration(duration_per_word).set_position('center')
                    clips.append(txt)
                    curr += duration_per_word

                final = CompositeVideoClip(clips)
                final.write_videofile("hasil.mp4", fps=24, codec="libx264")
                st.video("hasil.mp4")
            except Exception as e:
                st.error(f"Error: {e}")
