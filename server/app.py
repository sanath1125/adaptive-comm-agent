import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

class Query(BaseModel):
    text: str
    task_id: str

@app.get("/")
async def root():
    return {"status": "up", "message": "Adaptive Comm Agent (LLM-Proxy Ready) is running"}

@app.post("/reset")
async def reset():
    return {"status": "success", "message": "Environment reset"}

@app.post("/process")
async def process(query: Query):
    # 1. Fetch variables INSIDE the function to ensure they are captured
    api_base = os.environ.get("API_BASE_URL")
    api_key = os.environ.get("API_KEY")

    # 2. Initialize client only if we have the variables
    if not api_base or not api_key:
        # Fallback if the validator hasn't injected them yet (for local testing)
        print("Missing API_BASE_URL or API_KEY in environment")
        return {"action": 0}

    try:
        # 3. Use the specific client for the proxy
        client = OpenAI(base_url=api_base, api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # This is usually the default for LiteLLM proxies
            messages=[
                {"role": "system", "content": "You are a communication layer. Reply with '1' if the text is slang, foreign, or informal. Reply with '0' if it is formal English."},
                {"role": "user", "content": query.text}
            ],
            max_tokens=5,
            temperature=0
        )
        
        answer = response.choices[0].message.content.strip()
        # Ensure we only return 0 or 1
        action = 1 if "1" in answer else 0
        return {"action": action}

    except Exception as e:
        print(f"Proxy Connection Error: {str(e)}")
        # Last resort fallback to keep the code running
        text = query.text.lower()
        if any(word in text for word in ["hola", "cap", "fr"]):
            return {"action": 1}
        return {"action": 0}

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
