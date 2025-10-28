# Voice Assistant — Desktop Voice Assistant (Windows-focused)

**Author:** Saket Suryawanshi (cleaned & bug fixes)  
**Project:** Voice Assistant (generic, configurable assistant name)

---

## 🔊 Overview

This project is a local desktop Voice Assistant written in Python, designed for Windows. It supports both voice and text input and provides a set of productivity features such as web search, YouTube playback, weather lookup, Wikipedia summaries, note-taking, reminders, WolframAlpha queries, basic system controls and an optional Hugging Face chat integration.

This repository contains a cleaned, production-ready script and accompanying documentation to help you configure, run and extend the assistant.

---

## ✨ Key Features

- Dual input modes: voice (microphone) and text
- Play YouTube videos via `pywhatkit`
- Open common websites (YouTube, Google, Gmail, StackOverflow)
- Current weather lookup using OpenWeatherMap API
- Wikipedia summaries for quick facts
- Persistent notes (save & show)
- Reminders (minutes-based notifications)
- WolframAlpha for math and conversions
- Basic system controls (open Notepad, Calculator, VS Code, take screenshot, open Documents)
- Camera capture via `ecapture` (depends on OpenCV)
- Fuzzy intent detection for flexible natural-language commands
- Optional Hugging Face inference-based chat fallback

---

## 🧰 Requirements

- Python 3.8+ (tested on Windows)
- Recommended Python packages:

```bash
pip install pyautogui SpeechRecognition pyttsx3 wikipedia requests pywhatkit wolframalpha ecapture fuzzywuzzy python-Levenshtein
```

It is recommended to use a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create a `requirements.txt` for reproducibility.

---

## ⚙️ Configuration & API Keys

**Important:** Never commit API keys to a public repository. Use environment variables or a `.env` file (and add `.env` to `.gitignore`).

Configurable values in the script:

- `WEATHER_API_KEY` — OpenWeatherMap API key (required for weather).
- `WOLFRAM_APP_ID` — WolframAlpha App ID (required for Wolfram queries).
- `HF_API_TOKEN` — (Optional) Hugging Face API token for chat model access.
- `HF_CHAT_MODEL` — Default model endpoint (e.g. `google/gemma-2b-it`).
- `ASSISTANT_NAME` — Optional display name shown by the assistant (defaults to a generic "Voice Assistant").
- `NOTES_FILE` — Filename used for storing persistent notes (defaults to `assistant_notes.txt`).

### Set environment variables

**Windows (PowerShell):**
```powershell
$env:WEATHER_API_KEY="your_openweather_key"
$env:WOLFRAM_APP_ID="your_wolfram_app_id"
$env:HF_API_TOKEN="hf_ABC..."
```

**Windows (CMD):**
```cmd
set WEATHER_API_KEY=your_openweather_key
set WOLFRAM_APP_ID=your_wolfram_app_id
set HF_API_TOKEN=hf_ABC...
```

**macOS / Linux (bash):**
```bash
export WEATHER_API_KEY="your_openweather_key"
export WOLFRAM_APP_ID="your_wolfram_app_id"
export HF_API_TOKEN="hf_ABC..."
```

---

## 🚀 Running the Assistant

1. Save the assistant script (example `voice_assistant.py`) in your project folder.
2. Install required packages and set environment variables (see above).
3. Run:

```bash
python voice_assistant.py
```

On start-up you'll be greeted by voice and prompted to choose input mode:

- Enter `1` for Voice mode (microphone)
- Enter `2` for Text mode (keyboard)

---

## 🗣️ Example Commands & Usage

- `open youtube` — Open YouTube in the default browser
- `open google` — Open Google
- `search programming tutorials` — Perform a Google search
- `play <song name>` — Play a YouTube video via `pywhatkit`
- `weather` — Prompts for city and reads the current weather
- `wikipedia <query>` — Reads a short summary from Wikipedia
- `note` — Prompts to add a note; `note show` — lists saved notes
- `remind` — Set a minutes-based reminder
- `calculate <expression>` — Query WolframAlpha for computations or conversions
- `camera` or `take photo` — Capture a photo (requires camera and OpenCV)
- `screenshot` — Save a `screenshot.png` of the desktop

If an intent is not recognized, the assistant can optionally forward the query to a configured Hugging Face model to generate a fallback response.

---

## 🛠️ Troubleshooting

**Microphone / Recognition**
- Ensure microphone access and permissions are enabled.
- If `speech_recognition` raises errors, test with text mode or alternative audio backends.

**Text-to-Speech (TTS)**
- `pyttsx3` uses platform engines (SAPI5 on Windows). Confirm a working TTS voice is available.

**OpenWeather / Wolfram errors**
- Verify API keys and quotas. Ensure network connectivity.

**Hugging Face Chat**
- Anonymous HF inference may be rate-limited. Provide `HF_API_TOKEN` for reliable access.

**Application Launch Issues (VS Code, etc.)**
- The script attempts the `code` CLI and a common Windows install path. Modify paths if necessary.

**Camera / ecapture**
- Ensure OpenCV is installed and no other app is holding the camera.

---

## 📁 Notes & Files

Default files created by the assistant:

- `assistant_notes.txt` — persistent notes file (rename as desired)
- `screenshot.png` — created by screenshot command
- `photo.jpg` — created by camera capture

If you previously used a different notes filename (e.g., `g_one_notes.txt`), rename or migrate the file as needed.

Example one-liner (Windows PowerShell) to rename an existing notes file:
```powershell
if (Test-Path -Path "g_one_notes.txt") { Rename-Item -Path "g_one_notes.txt" -NewName "assistant_notes.txt" }
```

---

## 🔐 Security & Privacy

- Do not commit API keys or other secrets.
- Voice data is processed locally where possible, but services like Google Speech Recognition and Hugging Face inference send audio/text over the network — avoid sending private or sensitive data.
- Consider logging/retention policies for saved notes, transcripts or audio recordings.

---

## 💬 Extending & Customizing

- Add or refine intents in the `detect_intent` function.
- Replace fuzzy matching with a trained intent classifier for higher accuracy.
- Add calendar, email, or task integrations.
- Implement a GUI (tray app, system notification integration) for easier use.
- Add wake-word detection or persistent background listening (careful with privacy).

---

## 🧩 Contribution

1. Fork the repository.
2. Create a branch: `git checkout -b feature/my-feature`.
3. Commit your changes: `git commit -m "Add my feature"`.
4. Push and open a Pull Request.

Please open issues for bug reports or features.

---

## 📜 License

This project is offered under the **MIT License**. Include a `LICENSE` file in the repo.

---

## 🧑‍💻 Author & Credits

**Author:** Saket Suryawanshi — cleaned & bug fixes.  
If you redistribute or share, please credit the author.

---

## 🖼️ Screenshots / Demo

Include screenshots or a short GIF in `/screenshots` (optional but recommended).

```
/screenshots/assistant-demo.gif
/screenshots/assistant-screenshot.png
```

---

## ✅ Quick Git commands

```bash
git add README.md voice_assistant.py requirements.txt
git commit -m "Add README and Voice Assistant script"
git push origin main
```

---

## Changelog (short)

- General cleanup and bug fixes.
- Configurable assistant display name (`ASSISTANT_NAME`) and standardized notes filename `assistant_notes.txt`.
- Robust TTS initialization, fuzzy intent matching, and optional HF fallback.

---

**Thank you — and remember to remove API keys before pushing to any remote repository.**
