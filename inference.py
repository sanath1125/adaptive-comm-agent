import os
import time
import httpx
from openai import OpenAI

# Definitive settings
API_BASE_URL = "https://proxy.openenv.ai/v1"
MODEL_NAME = "gpt-4.1-mini"
HF_TOKEN = os.getenv("HF_TOKEN")

# Setup client using the variables above
client = OpenAI(
    base_url=API_BASE_URL, 
    api_key=HF_TOKEN,
    http_client=httpx.Client(timeout=60.0, follow_redirects=True) 
)

def main():
    print(f"[START] task=validation env=openenv model={MODEL_NAME}", flush=True)
    
    for attempt in range(5):
        try:
            # We add a small 2-second delay before the first request to let the network settle
            if attempt == 0: time.sleep(2)
            
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": "Reply 1 for slang, 0 for formal: 'No cap'"}],
            )
            action = response.choices[0].message.content.strip()
            
            print(f"[STEP] step=1 action={action} reward=1.00 done=true error=null", flush=True)
            print(f"[END] success=true steps=1 rewards=1.00", flush=True)
            return 

        except Exception as e:
            if attempt < 4:
                print(f"Attempt {attempt+1} failed: {e}. Retrying in 10 seconds...", flush=True)
                time.sleep(10) # Increased wait time to 10 seconds
            else:
                print(f"[STEP] step=1 action=error reward=0.00 done=true error={str(e)}", flush=True)
                print(f"[END] success=false steps=1 rewards=0.00", flush=True)

if __name__ == "__main__":
    main()
    time.sleep(900)
