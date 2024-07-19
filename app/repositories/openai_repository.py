import openai
from config import config

openai.api_key = config.OPENAI_API_KEY

def get_chatgpt_response(question):
    print("Sending request to OpenAI API with question:", question)
    response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question}
                    ],
                }
            ],
        )
    print("Received response from OpenAI API.", response.choices[0].message.content)
    return response.choices[0].message.content
