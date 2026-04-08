import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

class Query(BaseModel):
    text: str
    task_id: str

@app.get("/")
async def root():
    # Diagnostic check for the proxy variables
    return {"status": "active", "proxy": os.environ.get("API_BASE_URL") is not None}

@app.post("/reset")
async def reset():
    return {"status": "success"}

@app.post("/process")
async def process(query: Query):
    # FORCE read environment variables inside the request
    # This prevents the 'Bypass' error if the validator injects them late
    api_url = os.environ.get("API_BASE_URL")
    api_key = os.environ.get("API_KEY")

    if not api_url or not api_key:
        return {"action": 0}

    # Standardize the URL for the LiteLLM proxy
    if not api_url.endswith("/v1") and "huggingface.co" not in api_url:
        api_url = api_url.rstrip("/") + "/v1"

    try:
        # Initialize client INSIDE the process call
        client = OpenAI(base_url=api_url, api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a classifier. Respond ONLY with 1 for slang/informal or 0 for formal English."},
                {"role": "user", "content": query.text}
            ],
            max_tokens=2,
            temperature=0
        )
        
        result = response.choices[0].message.content.strip()
        # Return 1 if the LLM says 1, else 0
        return {"action": 1 if "1" in result else 0}

    except Exception as e:
        print(f"Proxy Error: {e}")
        return {"action": 0}

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    main()
