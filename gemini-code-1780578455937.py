import streamlit as st
import openai
from moviepy.editor import VideoFileClip
import os

st.set_page_config(page_title="Stream Clip AI", page_icon="⚡", layout="wide")

st.title("⚡ Ultra-Stream-Clip Generator (German Meta Edition)")
st.write("Verwandle chaotische, lustige Stream-Momente in virale TikToks im Stil von Kai Cenat, Speed & Co.")

# Sidebar für API Key
with st.sidebar:
    st.header("🔑 Setup")
    api_key = st.text_input("OpenAI API Key:", type="password")
    if api_key:
        openai.api_key = api_key

# Hauptbereich
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎥 Video-Upload")
    uploaded_file = f = st.file_uploader("Lade das Stream-Highlight hoch (MP4)", type=["mp4"])
    video_beschreibung = st.text_area("Was passiert im Clip? (z.B. 'Melo schreit herum wegen Fail' oder 'Absurde Ansage')", height=100)

if uploaded_file and api_key and video_beschreibung:
    with col1:
        with open("temp_stream_clip.mp4", "wb") as f:
            f.write(uploaded_file.read())
        st.video("temp_stream_clip.mp4")
        
        generate_btn = st.button("🚀 Clip optimieren & Analyse starten", use_container_width=True)

    if generate_btn:
        with col2:
            with st.spinner("🔥 Algorithmus-Analyse läuft..."):
                
                # Extrem geschärfter Prompt für lauten, lustigen deutschen Streamer-Content
                prompt = f"""
                Du bist der beste Social-Media-Manager für deutsche Stream-Highlights (Stil: Kai Cenat, IShowSpeed, Adin Ross angepasst auf die deutsche Twitch/Kick-Kultur).
                Der eingereichte Clip zeigt folgendes Ereignis: '{video_beschreibung}'.
                
                Erstelle ein perfektes Metadaten-Paket für TikTok und Instagram Reels:
                
                1. 🔥 3 x VIRALE HOOK-TITEL (Nutze Emojis, Capslock, extreme Wörter wie 'WILD', 'GEZINKT', 'ABGELENKT', 'GEBROCHEN' – perfekt für Text-Overlays im Video).
                2. 📝 DESCRIPTION: Eine kurze, extrem unterhaltsame Videobeschreibung mit einem starken Call to Action (z.B. 'Schick das einem Kumpel, der genauso goofy ist' oder 'Markiert euren Lieblings-Streamer').
                3. #️⃣ HASHTAGS: Die 6 besten Hashtags für die deutsche Gaming/Streaming-FYP.
                4. 📈 VIRAL-PROGNOSE (0-100% Score): Schätze ein, wie hoch die Chance ist, dass dieser Clip wegen 'Loud-Budget', absurden Reaktionen oder Chat-Interaktion viral geht und WARUM die Retention (Zuschauerbindung) hier hoch sein wird.
                """
                
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                analyse_ergebnis = response.choices[0].message.content
                
                st.subheader("📊 Virale Auswertung & Hooks")
                st.markdown(analyse_ergebnis)
                
            with st.spinner("✂️ Schneide Video auf TikTok-Format (9:16)..."):
                # Erste 20 Sekunden für maximalen Fokus auf die Reaction schneiden
                clip = VideoFileClip("temp_stream_clip.mp4").subclip(0, min(20, VideoFileClip("temp_stream_clip.mp4").duration))
                
                # Automatischer Fokus auf die Mitte (wo der Streamer meistens sitzt) -> 9:16 Crop
                w, h = clip.size
                target_w = int(h * (9/16))
                x_start = int((w - target_w) / 2)
                
                clip_cropped = clip.crop(x1=x_start, y1=0, x2=x_start + target_w, y2=h)
                clip_cropped.write_videofile("stream_export.mp4", codec="libx264", audio_codec="aac")
                
                st.subheader("🎬 Fertiges 9:16 Video für TikTok")
                st.video("stream_export.mp4")
                
                os.remove("temp_stream_clip.mp4")