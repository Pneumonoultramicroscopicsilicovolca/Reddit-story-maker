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
model = genai.GenerativeModel('models/gemini-1.5-flash')

st.title("🎬 Viral One-Word Subtitle Creator")

topic = st.text_input("Topik Cerita (Contoh: Horror story in a mall):")

def get_video(query):
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=portrait"
    try:
        r = requests.get(url, headers=headers)
        return r.json()['videos'][0]['video_files'][0]['link']
    except:
        return None

async def make_voice(text):
    cmt = Communicate(text, "en-US-ChristopherNeural")
    await cmt.save("suara.mp3")

if st.button("🚀 Generate Viral Video"):
    if not topic:
        st.error("Isi topik dulu bos!")
    else:
        with st.spinner("Lagi proses subtitle per kata..."):
            try:
                # 1. Bikin Cerita Panjang
                prompt = f"Write a long, gripping Reddit-style story about {topic}. Around 250 words, English."
                res = model.generate_content(prompt)
                cerita = res.text
                st.info("Cerita Berhasil Dibuat!")

                # 2. Bikin Suara
                asyncio.run(make_voice(cerita))
                audio = AudioFileClip("suara.mp3")
                durasi_total = audio.duration

                # 3. Ambil Video Background
                link = get_video("minecraft parkour") # Ganti tema di sini
                with open("bg.mp4", "wb") as f:
                    f.write(requests.get(link).content)

                # 4. Edit Video (Full Screen)
                video_awal = VideoFileClip("bg.mp4")
                if video_awal.duration < durasi_total:
                    video = video_awal.loop(duration=durasi_total).resize(height=1280)
                else:
                    video = video_awal.subclip(0, durasi_total).resize(height=1280)
                
                video = video.set_audio(audio)

                # 5. LOGIKA SUBTITLE PER KATA (Dynamic)
                words = cerita.split()
                duration_per_word = durasi_total / len(words)
                clips = [video]
                
                current_time = 0
                for word in words:
                    # Bikin teks per kata
                    txt = TextClip(word.upper(), fontsize=70, color='yellow', font='Arial-Bold',
                                   stroke_color='black', stroke_width=2).set_start(current_time).set_duration(duration_per_word).set_position('center')
                    clips.append(txt)
                    current_time += duration_per_word

                # Gabungkan video dengan ribuan potongan kata
                final_video = CompositeVideoClip(clips)
                final_video.write_videofile("output.mp4", fps=24, codec="libx264")

                st.video("output.mp4")
                st.success("Selesai! Subtitle muncul per kata!")

            except Exception as e:
                st.error(f"Error: {e}")
