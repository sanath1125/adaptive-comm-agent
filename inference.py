import os
import requests
import json
import sys

# Configuration
API_URL = os.getenv("API_BASE_URL", "https://newone1125-adaptive-comm-agent.hf.space")
PROCESS_URL = f"{API_URL}/process"

# The tasks defined in your openenv.yaml
TASKS = [
    {"id": "easy", "text": "Hello, how are you today?", "expected": 0},
    {"id": "medium", "text": "Hola, ¿cómo estás?", "expected": 1},
    {"id": "hard", "text": "That's no cap, for real fr.", "expected": 1}
]

def run_inference():
    total_score = 0
    
    for task in TASKS:
        # 1. MANDATORY [START] BLOCK
        print(f"[START] task={task['id']}", flush=True)
        
        try:
            payload = {"text": task['text'], "task_id": task['id']}
            response = requests.post(PROCESS_URL, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                action = result.get("action")
                
                # Calculate reward (1.0 if correct, 0.0 if wrong)
                reward = 1.0 if action == task['expected'] else 0.0
                total_score += reward
                
                # 2. MANDATORY [STEP] BLOCK
                # Even for single-step tasks, the validator needs to see this
                print(f"[STEP] step=1 reward={reward}", flush=True)
                
            else:
                print(f"[STEP] step=1 reward=0.0 error='HTTP {response.status_code}'", flush=True)
        
        except Exception as e:
            print(f"[STEP] step=1 reward=0.0 error='{str(e)}'", flush=True)
        
        # 3. MANDATORY [END] BLOCK
        # Note: 'score' here is usually the reward for that specific task
        task_score = 1.0 if (total_score > 0 and reward == 1.0) else 0.0
        print(f"[END] task={task['id']} score={task_score} steps=1", flush=True)

    # Final Summary (Optional but good practice)
    final_avg = total_score / len(TASKS)
    print(f"\nFinal Validation Score: {final_avg:.2f}")

if __name__ == "__main__":
    run_inference()
