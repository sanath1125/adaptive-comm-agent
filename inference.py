import os
import requests
import time
from huggingface_hub import InferenceClient

# ==========================================
# 1. ENVIRONMENT CONFIGURATION (Checklist Rules)
# ==========================================
# We use os.getenv so the judges can inject their own values during testing.
API_BASE_URL = os.getenv("API_BASE_URL", "https://newone1125-adaptive-comm-agent.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.1-8B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN") # DO NOT put your actual hf_xxx token here string!

# Initialize the Client
# Using the API_BASE_URL as the model for the client
client = InferenceClient(model=API_BASE_URL, token=HF_TOKEN)

# ==========================================
# 2. TEST TASKS (The 3.0/3.0 Logic)
# ==========================================
TASKS = [
    {
        "task": "Translate 'Hello, how are you?' to French.",
        "expected_action": 1,
        "description": "Simple Translation"
    },
    {
        "task": "What is the capital of France?",
        "expected_action": 0,
        "description": "General Knowledge (No Translation)"
    },
    {
        "task": "Can you help me translate this document to Spanish?",
        "expected_action": 1,
        "description": "Translation Request"
    }
]

def run_inference_test():
    print(f"🚀 Starting Inference Test on: {API_BASE_URL}")
    print("-" * 50)
    
    score = 0.0
    
    for i, t in enumerate(TASKS):
        print(f"Task {i+1}: {t['description']}")
        print(f"Input: {t['task']}")
        
        try:
            # Send request to your FastAPI server
            response = requests.post(
                f"{API_BASE_URL}/infer",
                json={"message": t["task"]},
                headers={"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
            )
            
            if response.status_code == 200:
                result = response.json()
                actual_action = result.get("action")
                
                print(f"Response: {result.get('response')}")
                print(f"Action Taken: {actual_action} (Expected: {t['expected_action']})")
                
                if actual_action == t['expected_action']:
                    print("✅ PASS")
                    score += 1.0
                else:
                    print("❌ FAIL (Wrong Action)")
            else:
                print(f"❌ FAIL (Server Error: {response.status_code})")
                
        except Exception as e:
            print(f"❌ CONNECTION ERROR: {e}")
            
        print("-" * 50)

    print(f"🏁 FINAL SCORE: {score}/{len(TASKS)}")
    return score

if __name__ == "__main__":
    run_inference_test()
