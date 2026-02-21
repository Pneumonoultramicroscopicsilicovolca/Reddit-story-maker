import streamlit as st
import openai
import asyncio
import edge_tts
import requests
import os
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AI Reddit Video Maker", page_icon="🎬")
st.title("🎬 Reddit Story Cloud Generator")
st.markdown("Generate viral Reddit stories with Minecraft parkour backgrounds automatically.")

# --- SIDEBAR UNTUK API KEYS ---
with st.sidebar:
    st.header("API Configuration")
    openai_key = st.text_input("OpenAI API Key", type="password")
    pexels_key = st.text_input("Pexels API Key", type="password")
    st.info("Get Pexels key for free at pexels.com/api")

# --- LOGIKA UTAMA ---
class CloudAutomator:
    def __init__(self, o_key, p_key):
        self.o_key = o_key
        self.p_key = p_key
        openai.api_key = o_key

    async def fetch_assets(self, topic):
        # 1. Generate Cerita (AI)
        prompt = f"Write a viral Reddit story about {topic} in English. Length: 2 minutes (approx 400 words). Use 'I' perspective."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        script = response.choices[0].message.content

        # 2. Cari Video Parkour (Pexels)
        headers = {"Authorization": self.p_key}
        v_req = requests.get(
            f"https://api.pexels.com/v1/search?query=minecraft+parkour&orientation=portrait&per_page=1", 
            headers=headers
        ).json()
        v_url = v_req['videos'][0]['video_files'][0]['link']
        
        with open("bg.mp4", "wb") as f:
            f.write(requests.get(v_url).content)
            
        return script

    async def render_process(self, script):
        # 3. Text to Speech (Edge-TTS)
        communicate = edge_tts.Communicate(script, "en-US-EricNeural")
        await communicate.save("voice.mp3")
        
        # 4. Rendering Video
        audio = AudioFileClip("voice.mp3")
        video = VideoFileClip("bg.mp4").loop(duration=audio.duration)
        
        # Subtitle sederhana di tengah
        txt = TextClip(
            script, fontsize=50, color='yellow', 
            method='caption', size=(video.w*0.8, None)
        ).set_duration(audio.duration).set_position('center')
        
        final = CompositeVideoClip([video, txt]).set_audio(audio)
        output_path = "viral_video.mp4"
        final.write_videofile(output_path, fps=24, codec="libx264")
        return output_path

# --- UI INTERFACE ---
topic = st.selectbox("Select Topic:", ["Revenge", "AmITheAsshole", "Success Story", "Scary Stories"])
if st.button("Generate & Render Video"):
    if not openai_key or not pexels_key:
        st.error("Please enter your API keys first!")
    else:
        automator = CloudAutomator(openai_key, pexels_key)
        with st.status("Processing..."):
            st.write("Writing script & fetching video...")
            script = asyncio.run(automator.fetch_assets(topic))
            
            st.write("Rendering (this might take a few minutes)...")
            video_file = asyncio.run(automator.render_process(script))
            
        st.success("Video successfully created!")
        st.video(video_file)
        
        with open(video_file, "rb") as file:
            st.download_button("Download Video", file, "reddit_story.mp4", "video/mp4")
