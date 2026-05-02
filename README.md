# 🚀 AI Resume Analyzer & Career Coach

An advanced, multi-modal AI platform designed to automate the recruitment screening process and provide interactive, voice-enabled career coaching to candidates. This project bridges the gap between static resume parsing and dynamic AI conversation, acting as both an automated HR screening tool and a personalized career counselor.

---

## 🌟 Core Features & Capabilities

### 🔍 Deep Resume Parsing & Skill Extraction
The AI goes beyond simple keyword matching. It extracts an exhaustive list of 15-20+ technical and soft skills, automatically categorizes them (e.g., Programming, Cloud, Soft Skills), and intelligently assigns a **Proficiency Level** (Beginner to Expert) based on the contextual evidence in the candidate's experience.

### 🗺️ 5-Tier Career Architecture Mapping
The system evaluates the profile against the global job market to predict **exactly 5 diverse career pathways**:
1. **Primary Best Fit Role**
2. **Secondary Strong Fit**
3. **Tertiary Alternative**
4. **Lateral / Pivot Role** (For career changes)
5. **Aspirational / Stretch Role** (For climbing the ladder)

### 📈 Position-Wise Skill Gap Analysis & Learning Paths
For each of the 5 predicted roles, the AI performs a strict gap analysis comparing the candidate's skills to the industry requirements. It highlights **Matching Skills**, warns about **Critical Missing Skills**, and generates a customized **Learning Path** (actionable steps) to help the candidate secure the job.

### 📁 Automated HR Database Tracker
Every time a resume is processed, the system automatically logs the candidate's Name, Top Position, Match Percentage, and Skills into a local persistent database (`candidates_report.csv`). Recruiters can view this live database in the sidebar and download it directly into Excel or Google Sheets with one click.

### 📊 Interactive Visual Analytics
The application uses Plotly to generate beautiful, highly reliable interactive charts:
- A **Donut Chart** showing the candidate's skill distribution.
- A **Bar Chart** organizing their proficiency levels.
- A **Radar Chart** scoring the candidate out of 100 on 5 core Data Analytics metrics.

### 🔊 ElevenLabs Voice AI Integrations
The application is fully integrated with studio-quality text-to-speech AI:
- **Career Pitch Generation:** Under each predicted role, a button allows the user to instantly generate and listen to a custom audio pitch explaining why they are a fit for that role.
- **Voice-Enabled Chatbot:** An interactive chatbot answers career questions and automatically reads its answers out loud using ElevenLabs.

### 📞 Real-Time Telephony Agent
Beyond the web dashboard, the project includes a separate backend script (`agent.py`) that acts as a real-time voice conversational agent using LiveKit. This allows a user to literally "talk" on a phone call or web stream to the AI Career Coach, powered by OpenAI and ElevenLabs.

---

## 🛠️ Technology Stack

This project is built using a modern, highly scalable AI stack:
- **Frontend / Dashboard:** `Streamlit` (Python)
- **Data Visualization:** `Plotly` & `Pandas`
- **PDF Extraction:** `PyPDF2`
- **LLM Engine (The "Brain"):** `gpt-4o-mini` routed through **OpenRouter**.
- **Voice Generation (TTS):** **ElevenLabs** API.
- **Real-Time Voice Infrastructure:** **LiveKit** & **Pipecat** (For sub-second latency voice conversations).

---

## ⚙️ Application Architecture

1. **`app (3).py` (The Core UI):** The main entry point for the Streamlit web application. It handles the UI layout, file uploading, database appending, data visualization, and ElevenLabs audio playback.
2. **`chatbot.py` (The AI Engine):** Contains heavily engineered System Prompts. It takes the raw PDF text, formats it, and forces the OpenAI model to return a highly structured JSON response containing the summary, skills, roles, gap analysis, and market insights.
3. **`agent.py` & `pipecat_agent.py`:** Backend scripts responsible for the real-time telephony/voice streaming infrastructure.
4. **`.env`:** Securely stores API keys (LiveKit, OpenRouter, ElevenLabs, Sarvam) out of the source code.

---

## 🚀 How to Run Locally

### 1. Install Dependencies
Make sure you are using Python 3.9+ (Note: LiveKit agents may have issues with Python 3.13, so 3.10-3.12 is recommended).
```bash
pip install streamlit pandas plotly PyPDF2 openai python-dotenv elevenlabs livekit-agents livekit-plugins-elevenlabs
```

### 2. Configure Environment Variables
Ensure your `.env` file contains your secure API keys:
```env
OPENAI_API_KEY=your_openrouter_or_openai_key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
ELEVENLABS_API_KEY=your_elevenlabs_key
LIVEKIT_API_KEY=your_livekit_key
LIVEKIT_API_SECRET=your_livekit_secret
LIVEKIT_URL=your_livekit_url
```

### 3. Launch the Web Dashboard
Run the Streamlit application to open the UI in your browser:
```bash
streamlit run "app (3).py"
```

### 4. Launch the Real-Time Voice Agent (Optional)
In a separate terminal, launch the LiveKit conversational agent:
```bash
python agent.py dev
```
*(Or use `python agent.py console` to test the agent purely in your terminal!)*

---

## 🎯 The Value Proposition
This platform solves a real-world B2B and B2C problem. 
- **For HR Departments:** An automated screening tool that instantly grades candidates, generates databases, and maps skill gaps.
- **For Job Seekers:** A premium career coach that builds learning paths and generates audio pitches to help candidates secure their dream jobs.
