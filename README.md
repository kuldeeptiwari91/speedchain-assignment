# 🦷 SmileCare Dental - AI Voice Receptionist

An AI-powered voice receptionist that handles dental appointment bookings through natural conversation. Built for the SpeedChain AI Full Stack Intern Assignment.

## 📹 Demo Video

[Watch Demo Video](your-loom-link-here)

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python 3.9+)
- Google Gemini 1.5 Flash (LLM)
- Google SpeechRecognition (STT)
- Google gTTS (TTS)
- Gmail SMTP (Email notifications)

**Frontend:**
- React.js
- Tailwind CSS

**Storage:**
- JSON files

## ✨ Features

- 🎤 Voice-to-voice conversation with AI receptionist
- 🧠 Context-aware dialogue with conversation memory
- 📅 Automatic appointment scheduling
- 📧 Email confirmations sent to patients
- 📊 Admin dashboard with analytics
- 📝 Full conversation transcripts

## 🚀 Setup & Run

### Prerequisites

- Python 3.9+
- Node.js 16+
- Gmail account
- Google Gemini API key ([Get free key](https://ai.google.dev/))

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys:
# - GEMINI_API_KEY (from https://ai.google.dev/)
# - SMTP_EMAIL (your Gmail)
# - SMTP_PASSWORD (Gmail App Password from https://myaccount.google.com/apppasswords)

# Create required directories
mkdir -p data static/audio

# Run server
uvicorn main:app --reload --port 8000
````

---

### Frontend Setup

Open a new terminal and run:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Then open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📂 Project Structure

```
speedchain-assignment/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── routes/                 # API endpoints
│   ├── services/               # AI services (STT, LLM, TTS)
│   ├── memory/                 # Conversation memory
│   └── data/                   # JSON storage
├── frontend/
│   ├── src/
│   │   └── components/         # React components
│   ├── package.json            # Node dependencies
│   └── public/
└── README.md
```

---

## 🎯 How It Works

1. 🗣️ User speaks into the microphone
2. 🧾 Google SpeechRecognition converts speech to text
3. 🧠 Google Gemini AI understands intent and generates a response
4. 🔊 gTTS converts the AI response to speech
5. 🎧 User hears the AI receptionist reply
6. 📅 System extracts appointment details and books automatically
7. 📧 Confirmation email is sent to the patient via Gmail SMTP

---

## 💡 Why These Technologies?

* 💸 **100% Free:** All services have generous free tiers
* 💳 **No Credit Card Required:** Perfect for development and demos
* ⚙️ **Production-Ready:** Built on Google’s reliable infrastructure
* ⚡ **Easy Setup:** Minimal configuration needed for quick deployment

---

## 📧 Gmail Setup

To enable email confirmations:

1. Enable **2-Factor Authentication** on your Google account
2. Go to **App Passwords**
3. Generate a password for **“Mail”**
4. Use this 16-character password in your `.env` file under `SMTP_PASSWORD`

---

## 🐛 Troubleshooting

**"Cannot connect to backend"**

* Ensure the backend server is running on port 8000

**"GEMINI_API_KEY not found"**

* Check that the `.env` file exists in the `backend/` folder
* Restart the backend server after editing `.env`

**"Microphone not working"**

* Allow microphone permissions in your browser
* Use Chrome or Edge for best compatibility

---

## 📄 License

**MIT License** — Free to use for personal and commercial projects.

---

## 👨‍💻 Author

**[Kuldeep Tiwari]**
GitHub: [@kuldeeptiwari91](https://github.com/kuldeeptiwari91)


