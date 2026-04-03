import os
import requests
from openai import OpenAI
from dotenv import load_dotenv  # 1. Imports the key-finding tool

load_dotenv()  # 2. Runs the tool to read your .env file

# OpenEnv Mandatory Configuration 
# This looks in .env first, then uses a default if .env is missing
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1/")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.1-8B-Instruct")
API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
SERVER_URL = "http://127.0.0.1:7860"

def main():
    print("--- 🚀 Starting OpenEnv Evaluation ---")
    resp = requests.post(f"{SERVER_URL}/reset")
    obs = resp.json()
    done = False
    total_reward = 0.0

    while not done:
        msg = obs["message_text"]
        task_id = obs["task_id"]
        print(f"\n📡 Task [{task_id}] | Message: '{msg}'")

        # The AI actually makes the choice here
        prompt = f"Analyze this message: '{msg}'. \nChoose: 0 (Pass), 1 (Translate), 2 (Summarize). \nReply with ONLY the digit."
        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=5
            )
            import re
            ai_content = completion.choices[0].message.content.strip()
            digits = re.findall(r'\d', ai_content)
            decision = int(digits[0]) if digits else 0
        except Exception as e:
            decision = 0 # Fallback

        step_resp = requests.post(f"{SERVER_URL}/step", json={"action_type": decision, "reasoning": "AI Decision"})
        result = step_resp.json()
        obs, reward, done = result["observation"], result["reward"], result["done"]
        total_reward += reward
        print(f"🤖 AI Action: {decision} | 🏆 Reward: {reward}")

    print(f"\n--- ✅ Final Score: {total_reward}/3.0 ---")

if __name__ == "__main__":
    main()