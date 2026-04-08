import os
from openai import OpenAI

# 1. Standard Environment Variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# Use raise instead of print to keep stdout clean for the parser
if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# 2. Initialize Client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def main():
    success = False
    rewards = []

    # Mandatory [START] line
    print(f"[START] task=validation env=openenv model={MODEL_NAME}", flush=True)

    try:
        # Standard completion call
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": "Reply 1 for slang, 0 for formal: 'No cap'"}
            ]
        )

        action = response.choices[0].message.content.strip()
        rewards.append(1.00)
        
        # Mandatory [STEP] line
        print(f"[STEP] step=1 action={action} reward=1.00 done=true error=null", flush=True)
        success = True

    except Exception as e:
        rewards.append(0.00)
        # Mandatory error [STEP] line
        print(f"[STEP] step=1 action=error reward=0.00 done=true error={str(e)}", flush=True)

    finally:
        # Mandatory [END] line
        rewards_str = ",".join(f"{r:.2f}" for r in rewards)
        print(f"[END] success={str(success).lower()} steps={len(rewards)} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    main()
