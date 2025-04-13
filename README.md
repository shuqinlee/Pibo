# Pibo - A Tiny Voice Buddy 🤖

**Pibo** is a playful, minimalist voice assistant built for curious tinkerers, indie devs, and anyone who’s ever wanted to talk to their computer on their own terms. No fees, no clouds, no nonsense — just real-time, natural conversation using only free and open tools. Total cost: **\$0**.

Originally crafted for Raspberry Pi, but runs anywhere.

中文版本见 https://github.com/shuqinlee/Pibo/blob/main/README-CN.md.
---

## ✨ Features

- 🎙️ **Real-Time Voice Detection**: Just talk — Pibo knows when you start and stop
- 🧠 **Smart Conversations**: Powered by Groq API + LLaMA 3.3 70B (or any Groq-supported model)
- 🔊 **High-Quality TTS**: Uses Minimax TTS to generate smooth, natural voice
- 🤫 **Silence Awareness**: Detects pauses
- 🧩 **Modular Design**: Easily extend, remix, or hack to your needs

---

## 🛠️ Under the Hood

- **Speech-to-Text (STT)**: Whisper Large V3 via Groq API (customizable)
- **Conversation Engine**: LLaMA 3.3 70B Versatile via Groq API (swap with other models as you wish)
- **Text-to-Speech (TTS)**: Browser-automated Minimax TTS with Playwright
- **Audio Playback**: PyGame for real-time audio feedback

---

## 🚀 Getting Started

### Requirements

- Python 3.8+
- Chrome browser (for Minimax TTS)
- Microphone

### Install

```bash
git clone https://github.com/shuqinlee/Pibo
cd Pibo
pip install -r requirements.txt
playwright install
```

### Configure

Create a `.env` file:

```
groq_api_key=your_groq_api_key
```

### Run

Start Chrome with remote debugging:

```bash
google-chrome --remote-debugging-port=9222
```

Run the assistant:

```bash
python voice_chat.py
```

💡 Tip: In mainland China, use `proxychains` or similar tools to access Groq API if needed.

Then start talking:

- You'll hear a chime
- Speak naturally — Pibo will detect when you stop
- It will respond automatically
- Press `Ctrl+C` to stop

---

## 🔧 Advanced Config

Edit the `Config` class to tweak:

- `model`: Any model supported by Groq API
- `max_turns`: Max number of dialogue turns
- `silence_threshold`: Silence detection sensitivity
- `silence_duration`: Pause duration before processing
- `save_dir`: Directory for saving audio

---

## 🔭 Future Plans (not guaranteed)
- 🗣️ **Voice Wake Word Support**: Add always-listening mode with hotword detection (e.g. "Hey Pibo") using lightweight wake-word engines like Porcupine, Snowboy, whisper-tiny

- 💬 **Personalized Chats**: Enable context-aware conversations that adapt based on the current time and prior interaction history, making Pibo feel more like a real companion. (Using techs like RAG, vector database)

- 📈 **Latency Analysis**: Measure and visualize each step (STT, LLM, TTS) in the pipeline to track and optimize response time.

- 🌊 **Streaming TTS**: Replace current block-based synthesis with streaming speech generation for ultra-smooth interactions.

- 🌍 **Offline Mode**: Explore lightweight offline options for edge devices.

- 🧪 **Multi-device Testing**: Optimize for different hardware including Raspberry Pi Zero, desktops, and laptops.

---

## 📄 License

MIT License

---

> *"Built for curiosity. Cost: \$0. Fun: priceless."*

