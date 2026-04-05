from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Data model for the incoming request
class Query(BaseModel):
    text: str
    task_id: str

@app.get("/")
async def root():
    return {"status": "up", "message": "Adaptive Comm Agent is running"}

@app.post("/reset")
async def reset():
    """Required by OpenEnv validator to reset the environment state"""
    return {"status": "success", "message": "Environment reset"}

@app.post("/process")
async def process(query: Query):
    """
    Your core logic: 
    0: Pass (Formal English)
    1: Action (Spanish or Slang)
    """
    text = query.text.lower()
    
    # Simple logic for the demo tasks
    if "hola" in text or "que tal" in text: # Spanish
        return {"action": 1}
    elif "no cap" in text or "fr" in text: # Slang
        return {"action": 1}
    else: # Standard English
        return {"action": 0}

# --- THE CRITICAL ADDITION BELOW ---
def main():
    import uvicorn
    # Starts the server on the port Hugging Face expects
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
