from app.repositories.openai_repository import get_chatgpt_response
from app.repositories.bedrock_repository import get_bedrock_response
import json

def process_chat_text(chat_text, provider="openai"):
    print(f"Getting LLM response using {provider}...")
    if provider == "openai":
        response = get_chatgpt_response(chat_text)
    elif provider == "bedrock":
        response = get_bedrock_response(chat_text)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    print("LLM response received:", response)

    return {
        "chat_text": chat_text,
        "response": response
    }

def extract_life_cycle_status(response):
        # Extract the value of the answer from the response
        lifeCycleStatus = response.split(":")[-1].strip()
        print("LifeCycleStatus:", lifeCycleStatus)
        return lifeCycleStatus

def extract_json_response(response):
    # Extract the value of the answer from the response
    # Always return a dict for downstream compatibility
    if isinstance(response, dict):
        return response
    if isinstance(response, str):
        # Try to extract JSON from string
        try:
            json_response = response.split("```json")[-1].strip().removesuffix("```")
            print("JSON Response:", json_response)
            return json.loads(json_response)
        except Exception as e:
            print("[ERROR] Could not parse JSON from string response:", e)
            return {"error": "Failed to parse response", "raw": response}
    return {"error": "Unsupported response type", "type": str(type(response)), "raw": str(response)}