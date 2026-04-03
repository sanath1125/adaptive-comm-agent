import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load the keys
load_dotenv()

# 2. Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1/")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.1-8B-Instruct")
API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def get_adaptive_action(message_text):
    """
    0: Standard English (No slang, no Spanish)
    1: Spanish OR Gen-Z Slang (mid, no cap, bounce, etc.)
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are a binary classifier. "
                        "If the message is standard, formal, or plain English with no slang, return '0'. "
                        "If the message contains ANY Spanish words OR Gen-Z slang, return '1'. "
                        "Output ONLY the single digit 0 or 1."
                    )
                },
                {"role": "user", "content": message_text}
            ],
            temperature=0.0
        )
        
        # Extract only the digit from the AI's response
        raw_output = response.choices[0].message.content.strip()
        if "1" in raw_output:
            return 1
        return 0
        
    except Exception as e:
        print(f"AI Error: {e}")
        return 0

if __name__ == "__main__":
    print(f"Test English: {get_adaptive_action('Hello, how are you?')}") # Should be 0
    print(f"Test Spanish: {get_adaptive_action('Hola')}") # Should be 1