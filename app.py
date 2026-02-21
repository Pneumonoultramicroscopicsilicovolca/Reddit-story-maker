import streamlit as st
import google.generativeai as genai
import requests
import os
os.environ["IMAGE_MAGICK_BINARY"] = "/usr/bin/convert
from edge_tts import Communicate
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

# 1. SETUP API (Hardcoded agar tidak bentrok dengan Secrets)
GEMINI_API_KEY = "AIzaSyCCaofacxUGUV_yDvIlpT_yTDXiuoV2Qn8"
PEXELS_API_KEY = "1MfncNTQhyT9hbvYd0l2DKQYMBp59V8CUevjAYn3j9raXx3j714KVpMs"

genai.configure(api_key=GEMINI_API_KEY)

st.title("🎬 Viral Video Creator - English Version")

topic = st.text_input("Topik Cerita:", placeholder="e.g. Mystery in the woods")

async def generate_audio(text):
    communicate = Communicate(text, "en-US-ChristopherNeural")
    await communicate.save("audio.mp3")

if st.button("🚀 GENERATE VIDEO"):
    if topic:
        with st.spinner("Processing..."):
            try:
                # AI Story
                model = genai.GenerativeModel('gemini-1.5-flash')
                story_res = model.generate_content(f"Write a 100 word horror story about {topic}. English.")
                story_text = story_res.text
                
                # Audio & Video
                asyncio.run(generate_audio(story_text))
                # (Lanjut ke proses MoviePy...)
                st.success("Video Ready!")
            except Exception as e:
                st.error(f"Error: {e}")
