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
    # Helps you check if the environment variables are active in HF logs
    return {"status": "up", "proxy_detected": "API_BASE_URL" in os.environ}

@app.post("/reset")
async def reset():
    return {"status": "success"}

@app.post("/process")
async def process(query: Query):
    # Fetching variables INSIDE the function to catch the validator's injection
    base_url = os.environ.get("API_BASE_URL")
    api_key = os.environ.get("API_KEY")

    if not base_url or not api_key:
        return {"action": 0}

    # Standardizing the URL for the OpenAI Client
    if not base_url.endswith("/v1") and "huggingface.co" not in base_url:
        base_url = base_url.rstrip("/") + "/v1"

    try:
        # Initialize client per-request to ensure the proxy 'handshake' is fresh
        client = OpenAI(base_url=base_url, api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a communication filter. Reply with 1 for slang/foreign language, 0 for formal English."},
                {"role": "user", "content": query.text}
            ],
            max_tokens=2,
            temperature=0
        )
        
        content = response.choices[0].message.content.strip()
        action = 1 if "1" in content else 0
        return {"action": action}

    except Exception as e:
        print(f"Proxy Error: {e}")
        return {"action": 0}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
