import os
from moviepy import VideoFileClip
from transcriber import transcribe_audio
from summarizer import summarize_text_llama3

#Workspace directory to store files
WORKSPACE_DIR = "workspace"
os.makedirs(WORKSPACE_DIR, exist_ok=True)

#File paths
video_path = os.path.join(WORKSPACE_DIR, "input_video.mp4")
audio_path = os.path.join(WORKSPACE_DIR, "output_audio.wav")
transcript_path = os.path.join(WORKSPACE_DIR, "transcript.txt")
summary_path = os.path.join(WORKSPACE_DIR, "summary.txt")

#Checking video exist
if not os.path.exists(video_path):
    print(f"❌ Error: No video found at {video_path}")
    print("👉 Please copy or rename your input video as:")
    print(f"   {video_path}")
    exit(1)

#Audio extraction
print("🎬 Extracting audio...")
video = VideoFileClip(video_path)
video.audio.write_audiofile(audio_path)

#Audio transcription
print("📝 Transcribing...")
transcript = transcribe_audio(audio_path)
with open(transcript_path, "w") as f:
    f.write(transcript)
print(f"✅ Transcript saved to {transcript_path}")

# Summarization using LLaMA
print("🧠 Summarizing with LLaMA 3...")
summary = summarize_text_llama3(transcript)
with open(summary_path, "w") as f:
    f.write(summary)
print(f"✅ Summary saved to {summary_path}")