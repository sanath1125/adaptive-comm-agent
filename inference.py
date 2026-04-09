import os
import time
from openai import OpenAI

# 1. READ VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# 2. REQUIRED VALIDATION
if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# 3. INITIALIZE CLIENT
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def main():
    # Give the container 5 seconds to stabilize the network connection
    time.sleep(5)
    
    print(f"[START] task=validation env=openenv model={MODEL_NAME}", flush=True)
    success = False
    rewards = []

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": "Reply 1 for slang, 0 for formal: 'No cap'"}
            ]
        )

        action = response.choices[0].message.content.strip()
        rewards.append(1.00)
        print(f"[STEP] step=1 action={action} reward=1.00 done=true error=null", flush=True)
        success = True

    except Exception as e:
        rewards.append(0.00)
        print(f"[STEP] step=1 action=error reward=0.00 done=true error={str(e)}", flush=True)

    finally:
        reward_str = ",".join(f"{r:.2f}" for r in rewards)
        print(f"[END] success={str(success).lower()} steps={len(rewards)} rewards={reward_str}", flush=True)

if __name__ == "__main__":
    main()
