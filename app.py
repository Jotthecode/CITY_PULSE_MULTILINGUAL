import os
import io
import tempfile
import json
import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import google.generativeai as genai
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech_v1beta1 as texttospeech
from google.api_core.exceptions import GoogleAPIError  # Corrected import for API errors

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="City Pulse Voice Agent",
    description="AI-powered multilingual city guide accessible via voice.",
    version="1.0.0"
)

# Mount static files (for index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")  # Templates for serving HTML

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Google Cloud clients
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

# Define tool using genai.protos
TOOLS = [
    genai.protos.Tool(
        function_declarations=[
            genai.protos.FunctionDeclaration(
                name="get_city_info",
                description="Provides general information about a city, such as its history, popular landmarks, or local culture.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "city_name": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="The name of the city the user is asking about.",
                        ),
                    },
                    required=["city_name"],
                ),
            )
        ]
    )
]

# Mock function for get_city_info
def get_city_info(city_name: str):
    if city_name.lower() == "rome":
        return {"info": "Rome is the capital city of Italy, known for its ancient history, iconic landmarks like the Colosseum and Roman Forum, and vibrant culture. It's often called the 'Eternal City'."}
    elif city_name.lower() == "paris":
        return {"info": "Paris is the capital of France, famous for the Eiffel Tower, Louvre Museum, and its romantic atmosphere. It's a global center for art, fashion, gastronomy, and culture."}
    elif city_name.lower() == "delhi":
        return {"info": "Delhi, India's capital territory, is a massive metropolitan area in the north of the country. It's a historic city with landmarks like India Gate, Red Fort, and Qutub Minar, blending ancient and modern cultures."}
    else:
        return {"info": f"I can tell you about {city_name}, but my knowledge for this city is general. It's a lovely city with its own unique charm."}

AVAILABLE_FUNCTIONS = {
    "get_city_info": get_city_info
}

system_instruction_text = (
    "You are City Pulse, an AI-powered multilingual city guide. "
    "Provide engaging, story-driven narratives and personalized recommendations. "
    "Focus on local secrets and immersive experiences. Speak in a friendly, helpful tone. "
    "If asked about a city, use the get_city_info tool. If the user doesn't specify a city, ask them which city they are interested in. "
    f"Today's date is {datetime.date.today().strftime('%B %d, %Y')}."
)

gemini_model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    tools=TOOLS,
    system_instruction=system_instruction_text
)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat-voice")
async def chat_voice(audio: UploadFile = File(...)):
    audio_content = await audio.read()

    # 1. Transcribe Audio
    try:
        audio_recognition = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=48000,
            language_code="en-IN",
            enable_automatic_punctuation=True,
        )
        response_asr = speech_client.recognize(config=config, audio=audio_recognition)

        if not response_asr.results:
            raise HTTPException(status_code=400, detail="Could not understand audio.")

        user_text = response_asr.results[0].alternatives[0].transcript
        print(f"User (Transcribed): {user_text}")

    except Exception as e:
        print(f"ASR Error: {e}")
        raise HTTPException(status_code=500, detail=f"ASR failed: {str(e)}")

    # 2. AI (Gemini)
    try:
        messages = [{"role": "user", "parts": [user_text]}]
        gemini_response = gemini_model.generate_content(messages)

        ai_text_response = ""
        tool_calls = []

        if gemini_response.candidates and gemini_response.candidates[0].content.parts:
            for part in gemini_response.candidates[0].content.parts:
                if part.function_call:
                    tool_calls.append(part.function_call)

        if tool_calls:
            function_responses = []
            for tool_call in tool_calls:
                function_name = tool_call.name
                function_args = {k: v for k, v in tool_call.args.items()}
                if function_name in AVAILABLE_FUNCTIONS:
                    result = AVAILABLE_FUNCTIONS[function_name](**function_args)
                    function_responses.append(genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=function_name,
                            response=result
                        )
                    ))
                else:
                    function_responses.append(genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=function_name,
                            response={"error": f"Tool '{function_name}' not implemented."}
                        )
                    ))

            follow_up = gemini_model.generate_content(messages + function_responses)
            ai_text_response = follow_up.candidates[0].content.parts[0].text
        else:
            ai_text_response = gemini_response.candidates[0].content.parts[0].text

        print(f"AI (Text): {ai_text_response}")

    except GoogleAPIError as e:
        print(f"Gemini API Error: {e}")
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")
    except Exception as e:
        print(f"Gemini General Error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected AI failure: {str(e)}")

    # 3. TTS (Text to Speech)
    try:
        synthesis_input = texttospeech.SynthesisInput(text=ai_text_response)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-IN",
            name="en-IN-Wavenet-B",
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
        )
        response_tts = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        audio_stream = io.BytesIO(response_tts.audio_content)

        return StreamingResponse(audio_stream, media_type="audio/wav", headers={
            "Content-Disposition": "inline; filename=response.wav"
        })

    except Exception as e:
        print(f"TTS Error: {e}")
        raise HTTPException(status_code=500, detail=f"TTS failed: {str(e)}")
