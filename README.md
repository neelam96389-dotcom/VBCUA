# 🎙️ Voice-Based Concept Understanding Analyser (VBCUA)

An AI-powered application that evaluates how well a user explains a technical concept through spoken audio — combining speech-to-text, semantic similarity, and audio fluency analysis into a single objective understanding score.

Built using **Streamlit**, **OpenAI Whisper**, **Sentence-BERT**, and **Librosa**.

---
## next
## next features

## 📌 Features

- 🎧 Audio upload & playback
- 📝 Speech-to-text transcription (OpenAI Whisper)
- 🧠 Semantic similarity scoring against a reference concept (Sentence-BERT)
- 📊 Audio feature extraction — filler word ratio, pause ratio, RMS energy (Librosa)
- ✅ Automated scoring engine (Strong / Moderate / Poor Understanding)
- 📈 Waveform visualization
- 📄 Downloadable PDF report (ReportLab)
- 🗂️ Session-based state — no login, no database required

---

## 🏗️ Project Architecture

```
User
  ↓
Streamlit UI
  ↓
Application Logic (same process — no separate backend service)
  ↓
Core Logic Service
 ├── Speech-to-Text (Whisper)
 ├── Semantic Similarity (Sentence-BERT)
 ├── Audio Feature Extraction (Librosa)
 ├── Scoring Engine
 └── PDF Report Generator (ReportLab)
  ↓
Streamlit Session State (in-memory)
```

---

## ⚙️ Technologies Used

| Technology | Purpose |
|---|---|
| Streamlit | Frontend UI & application runtime |
| OpenAI Whisper | Speech-to-text transcription |
| Sentence-Transformers (Sentence-BERT) | Semantic similarity scoring |
| Librosa / SoundFile | Audio feature extraction |
| Matplotlib | Waveform visualization |
| ReportLab | PDF report generation |
| Git & GitHub | Version control |

---

## 🚀 Installation & Run Instructions
## running all given instruction

### 1. Clone the Repository
```
git clone https://github.com/neelam96389-dotcom/VBCUA.git
cd "VBCUA/5. Project Development Phase/Source_Code"
```

### 2. Install ffmpeg (required by Whisper for audio decoding)
```
winget install ffmpeg
```

### 3. Create and Activate a Virtual Environment
```
python -m venv vbcu_env
vbcu_env\Scripts\activate
```

### 4. Install Dependencies
```
pip install -r requirements.txt
```

### 5. Run the Application
```
streamlit run app.py
```

Opens automatically at:
```
http://localhost:8501
```

> **Note:** The first analysis in a session will be slower, since Whisper and Sentence-BERT models are downloaded and loaded for the first time. Subsequent analyses in the same session are significantly faster.

---

## 🧪 Testing

The scoring engine was verified against a known worked example:

- Semantic Similarity: `0.03` · Filler Ratio: `0.03` · Pause Ratio: `0.11` · Energy: `0.1633`
- Result: **Final Score = 60/100 → Moderate Understanding** — matching the expected reference output exactly.

Audio feature extraction timing was measured directly on a 5-second test clip: ~2.1s on cold start (one-time library warmup), ~0.5s on subsequent calls within the same session.

Full details are documented in **`6. Project Testing/`**.

---

## 🌟 Future Enhancements

- Persistent storage (SQLite/PostgreSQL) for evaluation history across sessions
- Multilingual support
- Expanded reference concept bank beyond the current 3 concepts
- Real-time voice input with adaptive feedback

---

## 👨‍💻 Author

**Course:** Google Cloud Generative AI (SkillWallet)
**Team ID:** SWTID-2026-9706
**Project:** Voice-Based Concept Understanding Analyser (VBCUA)
College: University Maharani College
BCA

**Palak Suthar** 
GitHub: https://github.com/Palak-web021

**Neelam Kumari** 
Github: https://github.com/neelam96389-dotcom

---

## 📜 License

This project was developed as part of an educational SkillWallet Generative AI track submission.
