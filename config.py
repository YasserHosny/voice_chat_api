import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = Config()

print("Config loaded. OPENAI_API_KEY set.")
