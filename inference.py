import os
import requests
import sys

# Points to your local/hosted FastAPI server
API_URL = os.getenv("API_BASE_URL", "http://localhost:7860")

def run_validation():
    tasks = [
        {"id": "easy", "text": "Hello, how are you?", "expected": 0},
        {"id": "medium", "text": "Hola amigo!", "expected": 1},
        {"id": "hard", "text": "That's no cap fr", "expected": 1}
    ]

    for task in tasks:
        print(f"[START] task={task['id']}", flush=True)
        try:
            res = requests.post(f"{API_URL}/process", json={"text": task['text'], "task_id": task['id']}, timeout=10)
            action = res.json().get("action", 0)
            reward = 1.0 if action == task['expected'] else 0.0
            print(f"[STEP] step=1 reward={reward}", flush=True)
            print(f"[END] task={task['id']} score={reward} steps=1", flush=True)
        except Exception as e:
            print(f"[END] task={task['id']} score=0.0 steps=1 error='{e}'", flush=True)

if __name__ == "__main__":
    run_validation()
