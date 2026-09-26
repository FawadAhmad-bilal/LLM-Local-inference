# 🧠 Local LLM Chat — Streamlit + Ollama

A simple, fully offline Streamlit interface for chatting with a locally hosted LLM served by [Ollama](https://ollama.com). Built for the **Arch Technologies Generative AI Internship — Month 1, Task 1**.

## Features

- 🔌 Connects to a locally running Ollama server (`http://localhost:11434`) — no internet, no API key, no cost
- 💬 Chat-style interface with a text input box and response area
- 🕘 Conversation history panel that persists across messages in a session
- 🔄 Reset button to clear the conversation
- 🧩 Model picker — auto-detects every model you've pulled with Ollama and lets you switch between them

## Demo

*(Add a screenshot or GIF of the app here once you have one — drag an image into this section on GitHub.)*

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com/download) installed and running locally
- At least one model pulled via Ollama (e.g. `tinyllama`, `llama3`)

## Setup

1. **Install Ollama** (one-time): download from [ollama.com/download](https://ollama.com/download) and install it.

2. **Pull a model** — a small model like TinyLlama is a good starting point:
   ```bash
   ollama pull tinyllama
   ```

3. **Clone this repo and install Python dependencies:**
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   pip install -r requirements.txt
   ```

4. **Make sure Ollama is running** (it usually starts automatically after install; if not):
   ```bash
   ollama serve
   ```

5. **Run the app:**
   ```bash
   streamlit run app.py
   ```

   The app opens automatically in your browser at `http://localhost:8501`.

## Usage

- Pick a model from the sidebar dropdown (defaults to `tinyllama` if available).
- Type a question in the chat box at the bottom and press Enter.
- Your conversation history builds up above as you chat.
- Click **🔄 Reset conversation** in the sidebar to start fresh.

## How it works

The app sends your prompt to Ollama's local REST API (`/api/generate`) and displays the returned text. Since everything runs on your own machine, no data ever leaves your computer — this is a fully offline inference pipeline.

```
Streamlit (frontend, port 8501)  →  HTTP request  →  Ollama server (localhost:11434)  →  Local LLM
```

## Project structure

```
.
├── app.py              # Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           
```

## Notes

- Small models (like TinyLlama) are optimized for speed and low resource use, not answer quality — expect basic, sometimes imperfect responses. Swap in a larger model (`ollama pull llama3`) for better output if your hardware supports it.
- To store models on a different drive (useful if disk space is limited on `C:`), set the `OLLAMA_MODELS` environment variable to a folder on another drive before pulling any models.

## License

This project was built for educational purposes as part of an AI internship assignment.
