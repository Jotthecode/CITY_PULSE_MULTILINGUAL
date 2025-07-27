1. Project Title
City Pulse: Multilingual Voice Agent MVP
 2. Objective
To develop a minimal viable product (MVP) of a multilingual voice agent that allows users to speak in any supported language and receive spoken responses powered by OpenAI and Google Cloud APIs.
The goal is to enable a natural voice-based interaction that is language-agnostic, simple to use, and easily extendable.

3. Technologies Used
Layer
Technology
Backend Server
FastAPI (Python)
Voice Recognition
Google Cloud Speech-to-Text
Voice Synthesis
Google Cloud Text-to-Speech
Language AI
OpenAI GPT (text generation)
Frontend
HTML, JavaScript (Voice Recorder)
Storage / Secrets
.env, Git Ignore, Push Protection
Hosting (local)
Uvicorn development server

 4. Functional Workflow
User presses a button on the web interface to record speech.


The browser captures audio and sends it to the backend (/chat-voice).


Backend converts audio to text using Google Speech-to-Text.


The resulting text is passed to OpenAI for natural language generation.


OpenAI's reply is converted back into speech using Google Text-to-Speech.


The audio response is returned and played in the browser.



 5. MVP Feature Checklist
Feature
Status
FastAPI backend for voice processing
✅ Complete
HTML + JS frontend with microphone support
✅ Complete
Speech-to-text via Google Cloud
✅ Complete
OpenAI GPT-based response
✅ Complete
Text-to-speech using Google Cloud TTS
✅ Complete
Audio response playback in browser
✅ Complete
Multilingual language support
✅ Complete
Secure handling of .env and credentials
✅ Complete
GitHub push protection configured
✅ Complete
Cleaned Git history (no secrets exposed)
✅ Complete
Project documentation + submission file
✅ Complete


 6. Repository Structure
bash
CopyEdit
CITY_PULSE_MULTILINGUAL/
├── app.py                    # FastAPI backend
├── static/index.html        # Frontend UI
├── requirements.txt         # Dependencies
├── .env                     # Secrets (ignored)
├── .gitignore               # Prevents secret leaks
├── README.md                # Project overview
├── CityPulse_Submission.md  # <== This document


7. Security & GitHub Push Fixes
Issue: GitHub rejected a push due to service_account_key.json being committed.


Fix:


Secrets removed from Git history.


.gitignore updated to include .env and service_account_key.json.


GitHub push protection now passes.


Link: Push Protection Error Info



 8. Demo Video
https://github.com/Jotthecode/CITY_PULSE_MULTILINGUAL/blob/main/CITY_PULSE_MVP_VID.mp4


 9. Future Scope (Optional)
Deploy to cloud (e.g., Render, GCP)


Add GUI controls for selecting language


Multi-turn conversation history


Add LLM context for location-aware queries


Extend to mobile or kiosk interface



 10. Submission Link
GitHub Repository:
 🔗 https://github.com/Jotthecode/CITY_PULSE_MULTILINGUAL
