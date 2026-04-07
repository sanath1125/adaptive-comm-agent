import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# 1. Initialize the Client using the Proxy variables
# These are automatically provided by the Scaler validator
client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("API_KEY")
)

class Query(BaseModel):
    text: str
    task_id: str

@app.get("/")
async def root():
    return {"status": "up", "message": "Adaptive Comm Agent (LLM-Powered) is running"}

@app.post("/reset")
async def reset():
    return {"status": "success", "message": "Environment reset"}

@app.post("/process")
async def process(query: Query):
    """
    Using the LiteLLM Proxy to decide the action.
    """
    try:
        # 2. Make the API call through the proxy
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Use the model name suggested in your dashboard
            messages=[
                {"role": "system", "content": "You are a communication layer. Respond with '0' if the text is clear formal English. Respond with '1' if it is a foreign language, slang, or needs interpretation."},
                {"role": "user", "content": query.text}
            ],
            max_tokens=5
        )
        
        # 3. Parse the LLM's decision
        answer = response.choices[0].message.content.strip()
        action = 1 if "1" in answer else 0
        
        return {"action": action}
        
    except Exception as e:
        print(f"LLM Proxy Error: {e}")
        # Fallback to your manual logic if the proxy fails
        text = query.text.lower()
        if any(word in text for word in ["hola", "cap", "fr"]):
            return {"action": 1}
        return {"action": 0}

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
