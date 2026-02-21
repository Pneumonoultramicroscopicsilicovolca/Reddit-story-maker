import streamlit as st
import google.generativeai as genai
import requests
import os
from edge_tts import Communicate
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

# =========================================================
# CONFIGURATION
# =========================================================
GEMINI_API_KEY = "AIzaSyCCaofacxUGUV_yDvIlpT_yTDXiuoV2Qn8"
PEXELS_API_KEY = "1MfncNTQhyT9hbvYd0l2DKQYMBp59V8CUevjAYn3j9raXx3j714KVpMs"

genai.configure(api_key=GEMINI_API_KEY)
# Menggunakan model 'gemini-pro' agar lebih stabil di versi library apapun
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Reddit Story Generator", layout="centered")
st.title("🎬 Reddit Story Generator")
st.write("Create viral TikTok/Reels videos automatically!")

topic = st.text_area("Enter your topic or story prompt:", placeholder="Example: A story about a secret door...")

def get_pexels_video(query):
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=portrait"
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        if data.get('videos'):
            return data['videos'][0]['video_files'][0]['link']
    except:
        return None
    return None

async def generate_voice(text):
    communicate = Communicate(text, "en-US-ChristopherNeural")
    await communicate.save("audio.mp3")

if st.button("🚀 Generate Video"):
    if not topic:
        st.error("Please enter a topic first!")
    else:
        with st.spinner("Processing..."):
            try:
                # 1. Generate Story
                prompt = f"Write a short Reddit-style story about: {topic}. Max 40 words, English."
                response = model.generate_content(prompt)
                story = response.text
                st.info(f"Story: {story}")

                # 2. Generate Voice
                asyncio.run(generate_voice(story))

                # 3. Fetch Background Video
                video_url = get_pexels_video("parkour")
                if video_url:
                    with open("bg_video.mp4", "wb") as f:
                        f.write(requests.get(video_url).content)
                
                # 4. Video Editing
                audio = AudioFileClip("audio.mp3")
                video = VideoFileClip("bg_video.mp4").subclip(0, audio.duration).resize(height=1280)
                video = video.set_audio(audio)

                txt_clip = TextClip(story, fontsize=40, color='white', font='Arial-Bold', 
                                   method='caption', size=(video.w*0.8, None)).set_duration(audio.duration).set_position('center')
                
                final_video = CompositeVideoClip([video, txt_clip])
                final_video.write_videofile("final_output.mp4", fps=24, codec="libx264")

                st.video("final_output.mp4")
                st.success("Boom! Video Done!")
                
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.write("Engine: **Gemini Pro ⚡**")
