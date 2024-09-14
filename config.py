import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MARKER_PDF_API = os.getenv("MARKER_PDF_API")

config = Config()

print("Config loaded. OPENAI_API_KEY set.")
