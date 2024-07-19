from app.repositories.openai_repository import get_chatgpt_response
from app.utils.transcription import transcribe_audio

def process_voice_file(file):
    print("Transcribing audio file...")
    transcript = transcribe_audio(file)
    print("Transcription completed:", transcript)
    
    print("Getting ChatGPT response...")
    response = get_chatgpt_response(transcript)
    print("ChatGPT response received:", response)
    
    return {
        "transcript": transcript,
        "response": response
    }

