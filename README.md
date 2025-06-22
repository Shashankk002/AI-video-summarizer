# 🎥 AI Video Summarizer

A local, privacy-respecting tool that **transcribes and summarizes videos** using open-source AI models like **Whisper** and **LLaMA 3** — all wrapped in a clean **Streamlit interface**.

---

## 🚀 Features

- 🎬 Upload or paste a **YouTube link**
- 🎧 Extracts and transcribes audio using **Faster-Whisper**
- 🧠 Summarizes transcripts using **LLaMA 3 (via Ollama)**
- 💡 Fast, local-first, works offline once models are set up
- 🪄 Easy interface using **Streamlit**
- 📂 Downloadable transcript and summary files

---

## 📸 Demo

![screenshot](workspace/screenshot.png) <!-- Add a screenshot if you like -->

---

## ⚙️ Tech Stack

- [Streamlit](https://streamlit.io/) – UI framework
- [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) – transcription
- [LLaMA 3 via Ollama](https://ollama.com/) – text summarization
- [MoviePy](https://zulko.github.io/moviepy/) – audio extraction
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) – YouTube video downloading
- Python 🐍

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-video-summarizer.git
cd ai-video-summarizer

# Set up environment
pip install -r requirements.txt  # optional if you want to add one

# Run the app
streamlit run app.py