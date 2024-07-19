import speech_recognition as sr

def transcribe_audio(file):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(file)

    print("Recording audio from file...")
    with audio_file as source:
        audio = recognizer.record(source)

    print("Audio recorded. Transcribing...")
    try:
        transcript = recognizer.recognize_google(audio)
        print("Transcription successful:", transcript)
    except sr.UnknownValueError:
        transcript = "Could not understand the audio"
        print("Transcription failed: Could not understand the audio")
    except sr.RequestError:
        transcript = "Could not request results; check your network connection"
        print("Transcription failed: RequestError")

    return transcript

