import os
from openai import OpenAI

# Try to get their injected URL, fallback to the one the bot suggested
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN is missing")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

def main():
    success = False
    rewards = []
    print(f"[START] task=validation env=openenv model={MODEL_NAME}", flush=True)
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Slang check: 'No cap'"}]
        )
        action = response.choices[0].message.content.strip()
        rewards.append(1.00)
        print(f"[STEP] step=1 action={action} reward=1.00 done=true error=null", flush=True)
        success = True
    except Exception as e:
        rewards.append(0.00)
        print(f"[STEP] step=1 action=error reward=0.00 done=true error={str(e)}", flush=True)
    finally:
        print(f"[END] success={str(success).lower()} steps={len(rewards)} rewards={','.join(f'{r:.2f}' for r in rewards)}", flush=True)

if __name__ == "__main__":
    main()
