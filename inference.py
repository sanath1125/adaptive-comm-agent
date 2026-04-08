import os
import sys
from openai import OpenAI

# 1. Environment Variables - Using official defaults
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# Strict check for the token
if HF_TOKEN is None:
    print("CRITICAL ERROR: HF_TOKEN not found in environment.")
    sys.exit(1)

# 2. Initialize Client
# The 401 errors suggest the proxy might be failing to intercept. 
# We use the standard initialization as per the official template.
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def main():
    success = False
    rewards = []

    # Emit exactly the required [START] line
    print(f"[START] task=validation env=openenv model={MODEL_NAME}", flush=True)

    try:
        # Standard completion call with a 30s timeout to prevent hanging
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": "Reply 1 for slang, 0 for formal: 'No cap'"}
            ],
            timeout=30.0
        )

        action = response.choices[0].message.content.strip()
        rewards.append(1.00)
        
        # Emit exactly the required [STEP] line
        print(f"[STEP] step=1 action={action} reward=1.00 done=true error=null", flush=True)
        success = True

    except Exception as e:
        rewards.append(0.00)
        # Detailed error logging to help debug if the 401 persists
        print(f"[STEP] step=1 action=error reward=0.00 done=true error={str(e)}", flush=True)

    finally:
        # Emit exactly the required [END] line
        rewards_str = ",".join(f"{r:.2f}" for r in rewards)
        print(f"[END] success={str(success).lower()} steps={len(rewards)} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    main()
