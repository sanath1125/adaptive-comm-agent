from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn

app = FastAPI(title="Adaptive Comm Agent Environment")

# --- 1. OpenEnv Typed Models ---
class Observation(BaseModel):
    message_text: str
    task_id: str
    context: Optional[str] = None

class Action(BaseModel):
    action_type: int  # 0: Pass, 1: Translate/Interpret, 2: Summarize
    reasoning: str

class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]

# --- 2. 3-Tier Task Database ---
TASKS = {
    "easy": {
        "message": "Hello, how are you today?",
        "target_action": 0,  # Standard English -> Just Pass
        "description": "Standard formal communication"
    },
    "medium": {
        "message": "Hola, ¿cómo estás? Necesito ayuda.",
        "target_action": 1,  # Spanish -> Requires Translation
        "description": "Foreign language detection"
    },
    "hard": {
        "message": "That movie was mid, no cap. We should bounce.",
        "target_action": 1,  # Gen-Z Slang -> Requires Interpretation
        "description": "Nuanced informal slang detection"
    }
}

# --- 3. Environment State ---
class State:
    def __init__(self):
        self.current_task_idx = 0
        self.task_keys = list(TASKS.keys())
        self.done = False

state = State()

# --- 4. OpenEnv API Endpoints ---

@app.post("/reset", response_model=Observation)
async def reset():
    state.current_task_idx = 0
    state.done = False
    task_id = state.task_keys[state.current_task_idx]
    return Observation(
        message_text=TASKS[task_id]["message"],
        task_id=task_id
    )

@app.get("/state")
async def get_state():
    task_id = state.task_keys[state.current_task_idx]
    return {
        "task_id": task_id,
        "done": state.done,
        "progress": f"{state.current_task_idx + 1}/{len(state.task_keys)}"
    }

@app.post("/step", response_model=StepResponse)
async def step(action: Action):
    if state.done:
        raise HTTPException(status_code=400, detail="Episode already finished. Call /reset.")

    task_id = state.task_keys[state.current_task_idx]
    task_data = TASKS[task_id]

    # --- Meaningful Reward Function (Requirement) ---
    reward = 0.0
    if action.action_type == task_data["target_action"]:
        reward = 1.0
    else:
        # Penalize clearly wrong actions, but keep logic simple
        reward = 0.0

    # Move to next task
    state.current_task_idx += 1
    
    if state.current_task_idx >= len(state.task_keys):
        state.done = True
        # Return final state
        return StepResponse(
            observation=Observation(message_text="FINISHED", task_id="end"),
            reward=reward,
            done=True,
            info={"message": "All tasks completed"}
        )

    # Return next observation
    next_task_id = state.task_keys[state.current_task_idx]
    return StepResponse(
        observation=Observation(
            message_text=TASKS[next_task_id]["message"],
            task_id=next_task_id
        ),
        reward=reward,
        done=False,
        info={"last_action_correct": reward == 1.0}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)