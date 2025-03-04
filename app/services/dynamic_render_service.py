from app.repositories.openai_repository import get_chatgpt_response

def process_chat_text(chat_text):
    print("Getting ChatGPT response for chat text...")
    response = get_chatgpt_response(chat_text)
    print("ChatGPT response received:", response)
    
    return {
        "chat_text": chat_text,
        "response": response
    }