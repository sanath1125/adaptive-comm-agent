from pydantic import BaseModel
from typing import Optional, List

# 1. Action Model (What the Agent sends)
class CommAction(BaseModel):
    action_type: int 
    reasoning: Optional[str] = None

# 2. State Model (Server internal tracking)
class CommState(BaseModel):
    step_count: int
    total_reward: float
    history: List[str]
    current_task_id: str

# 3. Observation Model (What the Server sends back)
class CommObservation(BaseModel):
    message_text: str
    context: Optional[str] = None

# 4. Compatibility classes (To keep all scripts happy)
class AdaptiveCommAgentAction(CommAction):
    pass

class AdaptiveCommAgentObservation(CommObservation):
    pass