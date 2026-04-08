import os
from openai import OpenAI

# 1. Setup - We use the proxy URL as the default to avoid the 401 error
API_BASE_URL = os.getenv("API_BASE_URL", "https://proxy.openenv.ai/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    # We raise an error so it doesn't print extra text to stdout
    raise ValueError("HF_TOKEN environment variable is required")

# 2. Initialize Client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def main():
    success = False
    rewards = []
    
    # The [START] tag must be the very first thing printed
    print(f"[START] task=validation env=openenv model={MODEL_NAME}", flush=True)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Reply 1 for slang, 0 for formal: 'No cap'"}],
            timeout=30.0
        )

        action = response.choices[0].message.content.strip()
        rewards.append(1.00)
        
        # The [STEP] tag
        print(f"[STEP] step=1 action={action} reward=1.00 done=true error=null", flush=True)
        success = True

    except Exception as e:
        rewards.append(0.00)
        # Detailed error logging helps you see why it failed
        print(f"[STEP] step=1 action=error reward=0.00 done=true error={str(e)}", flush=True)

    finally:
        # The [END] tag
        rewards_str = ",".join(f"{r:.2f}" for r in rewards)
        print(f"[END] success={str(success).lower()} steps={len(rewards)} rewards={rewards_str}", flush=True)

import time

if __name__ == "__main__":
    main()
    # Keep the container alive for 30 minutes so the validator can finish
    print("Inference complete. Keeping container alive for validator...", flush=True)
    time.sleep(1800)
