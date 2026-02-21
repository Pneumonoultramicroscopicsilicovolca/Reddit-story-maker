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

# Kita pakai 'gemini-1.5-flash' tapi dengan library versi baru
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Reddit Story Generator", layout="centered")
st.title("🎬 Reddit Story Generator")

topic = st.text_area("Enter your story topic:", placeholder="Example: My wife stole my money...")

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
    await asyncio.wait_for(communicate.save("audio.mp3"), timeout=30)

if st.button("🚀 Generate Video"):
    if not topic:
        st.error("Enter a topic first!")
    else:
        with st.spinner("Magic in progress..."):
            try:
                # 1. Story
                prompt = f"Write a short, viral Reddit-style story about: {topic}. Max 40 words, English."
                response = model.generate_content(prompt)
                story_text = response.text
                st.info(f"Generated Story: {story_text}")

                # 2. Voice
                asyncio.run(generate_voice(story_text))

                # 3. Background
                video_url = get_pexels_video("parkour")
                if video_url:
                    with open("bg_video.mp4", "wb") as f:
                        f.write(requests.get(video_url).content)
                
                # 4. Editing
                audio = AudioFileClip("audio.mp3")
                video = VideoFileClip("bg_video.mp4").subclip(0, audio.duration).resize(height=1280)
                video = video.set_audio(audio)

                txt_clip = TextClip(story_text, fontsize=45, color='white', font='Arial-Bold', 
                                   method='caption', size=(video.w*0.8, None)).set_duration(audio.duration).set_position('center')
                
                final_video = CompositeVideoClip([video, txt_clip])
                final_video.write_videofile("final_output.mp4", fps=24, codec="libx264", audio_codec="aac")

                st.video("final_output.mp4")
                st.success("DONE! Enjoy your video!")
                
            except Exception as e:
                st.error(f"Error detail: {e}")

st.sidebar.write("Status: **Ready to Roll 🚀**")
