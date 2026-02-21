import streamlit as st
import openai
import requests
import os
from edge_tts import Communicate
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import random

# =========================================================
# API CONFIGURATION (HARDCODED)
# =========================================================
OPENAI_API_KEY = "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"
PEXELS_API_KEY = "1MfncNTQhyT9hbvYd0l2DKQYMBp59V8CUevjAYn3j9raXx3j714KVpMs"

openai.api_key = OPENAI_API_KEY

st.set_page_config(page_title="Reddit Story Generator", layout="centered")
st.title("🎬 Reddit Story Generator")
st.write("Create viral TikTok/Reels videos automatically!")

# Topic Input
topic = st.text_area("Enter your topic or story prompt:", placeholder="Example: A scary story about a haunted mall...")

def get_pexels_video(query):
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=portrait"
    r = requests.get(url, headers=headers)
    data = r.json()
    if data.get('videos'):
        return data['videos'][0]['video_files'][0]['link']
    return None

async def generate_voice(text):
    # Using English Voice for the story
    communicate = Communicate(text, "en-US-ChristopherNeural")
    await communicate.save("audio.mp3")

if st.button("🚀 Generate Video"):
    if not topic:
        st.error("Please enter a topic first!")
    else:
        with st.spinner("Processing your viral video..."):
            try:
                # 1. Generate Story using OpenAI (Requested in English)
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": f"Write a catchy Reddit-style short story about: {topic}. Keep it under 50 words and make it engaging."}]
                )
                story = response.choices[0].message.content
                st.info(f"Generated Story: {story}")

                # 2. Generate Voiceover
                asyncio.run(generate_voice(story))

                # 3. Fetch Background Video
                video_url = get_pexels_video("parkour")
                if video_url:
                    with open("bg_video.mp4", "wb") as f:
                        f.write(requests.get(video_url).content)
                
                # 4. Video Editing (MoviePy)
                audio = AudioFileClip("audio.mp3")
                video = VideoFileClip("bg_video.mp4").subclip(0, audio.duration).resize(height=1280)
                video = video.set_audio(audio)

                # Add Captions
                txt_clip = TextClip(story, fontsize=40, color='white', font='Arial-Bold', 
                                   method='caption', size=(video.w*0.8, None)).set_duration(audio.duration).set_position('center')
                
                final_video = CompositeVideoClip([video, txt_clip])
                final_video.write_videofile("final_output.mp4", fps=24, codec="libx264")

                st.video("final_output.mp4")
                st.success("Video Generated Successfully!")
                
            except Exception as e:
                st.error(f"Oops, something went wrong: {e}")

st.sidebar.markdown("---")
st.sidebar.write("System Status: **API Connected ✅**")
st.sidebar.write("Language: **English 🇺🇸**")

