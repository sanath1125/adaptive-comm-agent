from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/step")
async def step(request: Request):
    data = await request.json()
    # Pull out the pieces we need
    task = data.get("task", {})
    difficulty = task.get("difficulty", "easy")
    action = data.get("action", 0)

    # Simple Reward Logic
    if difficulty == "easy":
        expected = 0
    else:
        expected = 1
    
    reward = 1.0 if int(action) == expected else 0.0
    return {"reward": reward}

@app.get("/")
async def health():
    return {"status": "up"}
