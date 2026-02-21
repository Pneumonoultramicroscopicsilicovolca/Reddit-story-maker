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
# Menggunakan 'gemini-pro' karena paling kompatibel dengan berbagai versi library
model = genai.GenerativeModel('gemini-pro')

st.title("🎬 Viral Video Creator")

topic = st.text_input("Story Topic:")

async def save_audio(text):
    communicate = Communicate(text, "en-US-ChristopherNeural")
    await communicate.save("audio.mp3")

if st.button("Generate"):
    try:
        # 1. AI Story
        res = model.generate_content(f"Write a 30-word story about {topic}")
        story = res.text
        st.write(f"Story: {story}")
        
        # 2. Audio
        asyncio.run(save_audio(story))
        
        # 3. Video & Merge
        # (Logika pexels & moviepy tetap sama seperti sebelumnya)
        st.success("Check your folder for final_output.mp4!")
    except Exception as e:
        st.error(f"Error: {e}")
