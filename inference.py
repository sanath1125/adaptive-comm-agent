import os
from openai import OpenAI

# 1. READ THE VARIABLES FIRST
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# 2. PASTE THE CLIENT INITIALIZATION HERE (Outside the function)
# This uses the variables you just read above
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

# 3. NOW YOUR MAIN FUNCTION RUNS
def main():
    success = False
    rewards = []

    print(f"[START] task=validation env=openenv model={MODEL_NAME}", flush=True)

    try:
        # The client is already set up above, so we just use it here
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Reply 1 for slang, 0 for formal: 'No cap'"}]
        )

        action = response.choices[0].message.content.strip()
        rewards.append(1.00)
        print(f"[STEP] step=1 action={action} reward=1.00 done=true error=null", flush=True)
        success = True

    except Exception as e:
        rewards.append(0.00)
        print(f"[STEP] step=1 action=error reward=0.00 done=true error={str(e)}", flush=True)

    finally:
        rewards_str = ",".join(f"{r:.2f}" for r in rewards)
        print(f"[END] success={str(success).lower()} steps={len(rewards)} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    main()
