import requests

# 🏁 IMPORTANT: Replace with YOUR actual Hugging Face Space URL
SERVER_URL = "https://newone1125-adaptive-comm-agent.hf.space"

def main():
    print("--- 🚀 Starting OpenEnv Evaluation ---")
    
    # These are our 3 test cases
    tasks = [
        {"difficulty": "easy", "message": "Hello, how are you today?"},
        {"difficulty": "medium", "message": "Hola, ¿cómo estás? Necesito ayuda."},
        {"difficulty": "hard", "message": "That movie was mid, no cap. We should bounce."}
    ]
    
    total_reward = 0.0

    for task in tasks:
        print(f"\n📡 Task [{task['difficulty']}] | Message: '{task['message']}'")
        
        try:
            # 1. Ask the AI Agent (the Brain) what to do
            # Note: We import the logic from your local client.py to test
            from client import get_ai_action
            action = get_ai_action(task['message'])
            
            # 2. Send that action to the Hugging Face Judge (the Environment)
            payload = {
                "task": task,
                "action": action
            }
            response = requests.post(f"{SERVER_URL}/step", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                reward = result.get("reward", 0.0)
                total_reward += reward
                print(f"🤖 AI Action: {action} | 🏆 Reward: {reward}")
            else:
                print(f"❌ Server Error: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Error during task: {e}")

    print(f"\n--- ✅ Final Score: {total_reward}/{len(tasks)} ---")

if __name__ == "__main__":
    main()
