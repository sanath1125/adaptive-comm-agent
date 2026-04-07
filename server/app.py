import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

class Query(BaseModel):
    text: str
    task_id: str

@app.post("/process")
async def process(query: Query):
    base_url = os.environ.get("API_BASE_URL")
    api_key = os.environ.get("API_KEY")
    if not base_url or not api_key:
        return {"action": 0}
    
    # Standardize URL
    if not base_url.endswith("/v1") and "huggingface.co" not in base_url:
        base_url = base_url.rstrip("/") + "/v1"

    try:
        client = OpenAI(base_url=base_url, api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Reply 1 if slang/informal, 0 if formal: {query.text}"}],
            max_tokens=2
        )
        content = response.choices[0].message.content.strip()
        return {"action": 1 if "1" in content else 0}
    except:
        return {"action": 0}

@app.post("/reset")
async def reset():
    return {"status": "success"}

@app.get("/")
async def root():
    return {"status": "up"}

# THE ENTRY POINT
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
