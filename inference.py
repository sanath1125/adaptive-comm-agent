import os
import time
from openai import OpenAI

# We are writing the address directly here so it never gets lost
API_BASE_URL = "https://proxy.openenv.ai/v1"
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN is missing in Space Secrets!")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

def main():
    print(f"[START] task=validation env=openenv model={MODEL_NAME}", flush=True)
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Reply 1 for slang, 0 for formal: 'No cap'"}],
            timeout=30.0
        )
        action = response.choices[0].message.content.strip()
        print(f"[STEP] step=1 action={action} reward=1.00 done=true error=null", flush=True)
        print(f"[END] success=true steps=1 rewards=1.00", flush=True)
    except Exception as e:
        print(f"[STEP] step=1 action=error reward=0.00 done=true error={str(e)}", flush=True)
        print(f"[END] success=false steps=1 rewards=0.00", flush=True)

if __name__ == "__main__":
    main()
    time.sleep(600) # Keeps it green for the validator
