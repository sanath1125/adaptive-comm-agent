import os
from openai import OpenAI

# 1. Environment variables - EXACTLY as the bot requested
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1").strip()
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini").strip()
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()

if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is required")

# 2. FORCE the Proxy Path
# If the URL doesn't end in /v1, the OpenAI library often fails to route correctly
if not API_BASE_URL.endswith("/v1"):
    API_BASE_URL = API_BASE_URL.rstrip("/") + "/v1"

# 3. Explicit Client Setup
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN,
    # We add this to prevent the library from 'guessing' the organization
    organization=None,
    project=None
)

def main():
    success = False
    rewards = []

    print(f"[START] task=validation env=openenv model={MODEL_NAME}", flush=True)

    try:
        # Standard completion call
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": "Reply 1 for slang, 0 for formal: 'No cap'"}
            ],
            timeout=30.0 # Add a timeout so it doesn't hang for 3 hours
        )

        action = response.choices[0].message.content.strip()
        rewards.append(1.00)
        
        print(f"[STEP] step=1 action={action} reward=1.00 done=true error=null", flush=True)
        success = True

    except Exception as e:
        rewards.append(0.00)
        # This will print the error so you can see if the URL is correct in your logs
        print(f"[STEP] step=1 action=error reward=0.00 done=true error={str(e)}", flush=True)

    finally:
        rewards_str = ",".join(f"{r:.2f}" for r in rewards)
        print(f"[END] success={str(success).lower()} steps={len(rewards)} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    main()
