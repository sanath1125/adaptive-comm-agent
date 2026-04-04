import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("HF_TOKEN")

# The InferenceClient automatically uses the new router.huggingface.co
client = InferenceClient(api_key=token)

def get_ai_action(message):
    prompt = f"Classify: '{message}'. If formal English, output 0. If Spanish or Slang, output 1. Output ONLY the number 0 or 1."
    
    try:
        # We specify the model here; the client handles the routing logic
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1,
            temperature=0.1
        )
        
        content = response.choices[0].message.content.strip()
        # Clean up in case the AI adds a space or period
        digit = "".join(filter(str.isdigit, content))
        
        return int(digit) if digit in ["0", "1"] else 0
        
    except Exception as e:
        print(f"Agent Error: {e}")
        return 0
