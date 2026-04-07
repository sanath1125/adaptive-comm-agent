import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# Configuration - Using exact variable names from the Scaler instructions
API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.environ.get("API_KEY")

class Query(BaseModel):
    text: str
    task_id: str

@app.get("/")
async def root():
    return {"status": "up", "api_connected": bool(API_BASE_URL)}

@app.post("/reset")
async def reset():
    return {"status": "success"}

@app.post("/process")
async def process(query: Query):
    # Initialize the client strictly with the provided environment variables
    # We do NOT use a fallback here so the validator MUST see the traffic
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY
    )

    # Use a very specific prompt to ensure the LLM gives us a 0 or 1
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "You are a communication filter. If the text is informal, slang, or a foreign language, reply only with the number 1. If it is formal English, reply only with the number 0. Do not provide explanations."},
            {"role": "user", "content": query.text}
        ],
        max_tokens=2,
        temperature=0
    )
    
    # Extract the result
    llm_answer = response.choices[0].message.content.strip()
    
    # Final check: the validator expects an integer-like action
    action = 1 if "1" in llm_answer else 0
    
    return {"action": action}

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
