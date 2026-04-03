import random
import models # Directly from the root

class AdaptiveCommEnv:
    def __init__(self):
        self.tasks = [
            {"id": "task_1_easy_translate", "msg": "Hola, ¿cómo estás?", "lang": "Spanish", "slang": False, "target": "English", "correct": 1},
            {"id": "task_2_medium_slang", "msg": "That movie was mid, no cap.", "lang": "English", "slang": True, "target": "English", "correct": 2},
            {"id": "task_3_hard_simplify", "msg": "The biological repercussions of the atmospheric shift are non-negligible.", "lang": "English", "slang": False, "target": "English", "correct": 3}
        ]
        self.current_task_idx = 0
        self.state = models.CommState(step_count=0, total_reward=0.0, history=[], current_task_id="")

    def reset(self):
        self.current_task_idx = 0
        self.state = models.CommState(step_count=0, total_reward=0.0, history=[], current_task_id=self.tasks[0]["id"])
        return self._get_obs()

    def _get_obs(self):
        task = self.tasks[self.current_task_idx]
        return models.CommObservation(
            message_text=task["msg"],
            detected_language=task["lang"],
            user_preferred_lang=task["target"],
            is_slang_detected=task["slang"],
            context_type="General"
        )

    def step(self, action: models.CommAction):
        task = self.tasks[self.current_task_idx]
        reward = 1.0 if action.action_type == task["correct"] else 0.0
        self.state.total_reward += reward
        self.state.step_count += 1
        self.current_task_idx += 1
        done = self.current_task_idx >= len(self.tasks)
        return {"observation": self._get_obs() if not done else None, "reward": reward, "done": done}