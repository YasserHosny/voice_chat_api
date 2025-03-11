from app.repositories.openai_repository import get_chatgpt_response

def process_chat_text(chat_text):
    print("Getting ChatGPT response for chat text...")
    response = get_chatgpt_response(chat_text)
    print("ChatGPT response received:", response)
    
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
    json_response = response.split("```json")[-1].strip().removesuffix("```")
    print("JSON Response:", json_response)
    return json_response