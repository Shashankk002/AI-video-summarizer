import streamlit as st
import os
import yt_dlp
from moviepy import VideoFileClip
from transcriber import transcribe_audio
from summarizer import summarize_text_llama3

# --- Setup ---
WORKSPACE_DIR = "workspace"
os.makedirs(WORKSPACE_DIR, exist_ok=True)

video_path = os.path.join(WORKSPACE_DIR, "input_video.mp4")
audio_path = os.path.join(WORKSPACE_DIR, "output_audio.wav")
transcript_path = os.path.join(WORKSPACE_DIR, "transcript.txt")
summary_path = os.path.join(WORKSPACE_DIR, "summary.txt")

# --- Streamlit Page Settings ---
st.set_page_config(page_title="AI Video Summarizer")
st.title("🎥 AI Video Summarizer")
st.markdown("Upload a video file or paste a YouTube link — we'll transcribe and summarize it using local AI models (Whisper + LLaMA 3).")

# --- Initialize session state ---
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "video_source" not in st.session_state:
    st.session_state.video_source = None

# --- Input method selector ---
video_input_method = st.selectbox(
    "Select video input method:",
    ("Upload MP4 File", "Paste YouTube Link")
)

uploaded_file = None
youtube_url = ""
current_source = None

# --- Show input fields based on method ---
if video_input_method == "Upload MP4 File":
    uploaded_file = st.file_uploader("Upload your video:", type=["mp4"])
    if uploaded_file is not None:
        current_source = f"upload:{uploaded_file.name}_{uploaded_file.size}"

elif video_input_method == "Paste YouTube Link":
    youtube_url = st.text_input("Paste YouTube video link:")
    if youtube_url:
        current_source = f"youtube:{youtube_url.strip()}"

# --- Clear session cache if input source changes ---
if current_source and current_source != st.session_state.video_source:
    st.session_state.video_source = current_source
    st.session_state.transcript = None
    st.session_state.summary = None

# --- Process video input ---
video_ready = False

if video_input_method == "Upload MP4 File" and uploaded_file is not None:
    with st.spinner("📁 Saving uploaded video..."):
        try:
            if os.path.exists(video_path):
                os.remove(video_path)
            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())
            st.success("✅ Video uploaded successfully!")
            video_ready = True
        except Exception as e:
            st.error(f"❌ Failed to save uploaded file: {e}")

elif video_input_method == "Paste YouTube Link" and youtube_url:
    with st.spinner("📥 Downloading from YouTube..."):
        try:
            if os.path.exists(video_path):
                os.remove(video_path)
            ydl_opts = {
                'format': 'bestvideo+bestaudio',
                'outtmpl': video_path,
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            st.success("✅ YouTube video downloaded and converted to MP4!")
            video_ready = True
        except Exception as e:
            st.error(f"❌ Failed to download or process video: {e}")

# --- Run the pipeline if video is ready ---
if video_ready:
    # --- Extract audio ---
    with st.spinner("🎬 Extracting audio..."):
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)

    # --- Transcription ---
    st.subheader("📄 Transcript")
    if st.session_state.transcript is None:
        with st.spinner("📝 Transcribing audio..."):
            transcript = transcribe_audio(audio_path)
            st.session_state.transcript = transcript
            with open(transcript_path, "w") as f:
                f.write(transcript)
    else:
        transcript = st.session_state.transcript

    st.text_area("Transcript", transcript, height=250)
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.download_button("⬇️ Download Transcript", transcript, file_name="transcript.txt")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Summarization ---
    st.subheader("🧠 Summary")
    if st.session_state.summary is None:
        with st.spinner("🔎 Summarizing transcript with LLaMA 3..."):
            summary = summarize_text_llama3(transcript)
            st.session_state.summary = summary
            with open(summary_path, "w") as f:
                f.write(summary)
    else:
        summary = st.session_state.summary

    st.text_area("Summary", summary, height=200)
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.download_button("⬇️ Download Summary", summary, file_name="summary.txt")
    st.markdown("</div>", unsafe_allow_html=True)