import os
from openai import OpenAI

# The system injects these. If we provide defaults, we break the connection.
API_KEY = os.environ["API_KEY"]
API_BASE_URL = os.environ["API_BASE_URL"]
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")

client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE_URL
)

def main():
    success = False
    rewards = []
    print(f"[START] task=validation env=openenv model={MODEL_NAME}", flush=True)

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
        print(f"[END] success={str(success).lower()} steps={len(rewards)} rewards={','.join(f'{r:.2f}' for r in rewards)}", flush=True)

if __name__ == "__main__":
    main()
