# 🌆 City Pulse – Multilingual Voice Agent MVP

City Pulse is a multilingual voice assistant MVP built using FastAPI and OpenAI, designed to provide conversational responses in multiple languages. The application accepts user input via voice, transcribes it, generates a reply using OpenAI, and responds via synthesized speech.

---

## 🔗 Repository

GitHub: [CITY_PULSE_MULTILINGUAL](https://github.com/Jotthecode/CITY_PULSE_MULTILINGUAL)

---

## ⚙️ Tech Stack

- 🧠 OpenAI GPT for text generation
- 🔊 Google Cloud Text-to-Speech & Speech-to-Text
- 🌐 FastAPI as the backend server
- 🎙️ HTML + JavaScript frontend with voice recording
- 🐍 Python

---

## 🛠️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/Jotthecode/CITY_PULSE_MULTILINGUAL.git
   cd CITY_PULSE_MULTILINGUAL
Create and activate a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Add environment variables

Create a .env file:

ini
Copy
Edit
OPENAI_API_KEY=your_openai_api_key
Set up Google Cloud credentials

Create a service account in Google Cloud with access to Speech-to-Text and Text-to-Speech APIs.

Download the service_account_key.json file and set an environment variable:

bash
Copy
Edit
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service_account_key.json"
Run the application

bash
Copy
Edit
uvicorn app:app --reload
Visit in browser

bash
Copy
Edit
http://localhost:8000/static/index.html
✅ MVP Checklist
Feature	Status
FastAPI backend running	✅ Complete
HTML frontend with voice recording	✅ Complete
Audio upload via POST request	✅ Complete
Google Speech-to-Text integration	✅ Complete
Multilingual language support	✅ Complete
OpenAI GPT response generation	✅ Complete
Google Text-to-Speech response	✅ Complete
Audio response played in browser	✅ Complete
Environment variables via .env file	✅ Complete
.gitignore for secrets and cache	✅ Complete
Push protection & secret cleanup	✅ Fixed
README documentation	✅ You're here!

📁 File Structure
bash
Copy
Edit
city_pulse_mvp/
├── app.py
├── static/
│   └── index.html
├── service_account_key.json  # (ignored)
├── requirements.txt
├── .env                      # (ignored)
├── .gitignore
└── README.md
🔐 Security Notes
This project previously included a committed service_account_key.json file. It has been removed, and Git history has been cleaned. Ensure all future pushes exclude .env and secret key files.

.env and service_account_key.json are now in .gitignore

You can check GitHub's push protection page if needed.

✨ Contributions
PRs are welcome. Feel free to open issues or improvements on multilingual NLP, voice UIs, or AI integration.


