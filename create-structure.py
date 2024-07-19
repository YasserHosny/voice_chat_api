import os

# Define the directory structure
directories = [
    'voice_chat_api/app/api',
    'voice_chat_api/app/services',
    'voice_chat_api/app/repositories',
    'voice_chat_api/app/utils',
]

# Define the files and their content
files_content = {
    'voice_chat_api/config.py': '''\
import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = Config()
''',

    'voice_chat_api/run.py': '''\
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
''',

    'voice_chat_api/app/__init__.py': '''\
from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.api.voice import voice_bp
    app.register_blueprint(voice_bp, url_prefix='/api/voice')

    return app
''',

    'voice_chat_api/app/api/voice.py': '''\
from flask import Blueprint, request, jsonify
from app.services.voice_service import process_voice_file

voice_bp = Blueprint('voice_bp', __name__)

@voice_bp.route('/process', methods=['POST'])
def process_voice():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    response = process_voice_file(file)
    return jsonify(response)
''',

    'voice_chat_api/app/services/voice_service.py': '''\
from app.repositories.openai_repository import get_chatgpt_response
from app.utils.transcription import transcribe_audio

def process_voice_file(file):
    transcript = transcribe_audio(file)
    response = get_chatgpt_response(transcript)
    return {
        "transcript": transcript,
        "response": response
    }
''',

    'voice_chat_api/app/repositories/openai_repository.py': '''\
import openai
from config import config

openai.api_key = config.OPENAI_API_KEY

def get_chatgpt_response(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=150
    )
    return response.choices[0].text.strip()
''',

    'voice_chat_api/app/utils/transcription.py': '''\
import speech_recognition as sr

def transcribe_audio(file):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(file)

    with audio_file as source:
        audio = recognizer.record(source)

    try:
        transcript = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        transcript = "Could not understand the audio"
    except sr.RequestError:
        transcript = "Could not request results; check your network connection"

    return transcript
''',

    'voice_chat_api/requirements.txt': '''\
Flask==2.0.2
openai==1.35.7
SpeechRecognition==3.8.1
'''
}

# Create directories
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Create files with content
for file_path, content in files_content.items():
    with open(file_path, 'w') as file:
        file.write(content)

print("Project structure created successfully.")
