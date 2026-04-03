# Adaptive Communication Agent (OpenEnv) 🚀

A high-fidelity simulation environment for evaluating an LLM agent's ability to navigate complex, non-standard human communication. 

## 🌟 The Problem & Real-World Utility
In modern global communication, users often face "Language Friction." This environment models a **Communication Middleware Layer** that decides when to trigger expensive translation or interpretation services. 
- **Business Use-Case:** Reducing API costs for customer support platforms by filtering standard text while catching nuanced slang and foreign languages.

## 🏗️ Environment Architecture (OpenEnv Spec)
This project implements the full **OpenEnv** interface with typed Pydantic models for predictable, scalable agent interaction.

### 1. Task Hierarchy (Easy → Hard)
- **Task 1 (Easy):** "Standard English Check." Validates that the agent doesn't over-process simple data. (Target: Pass)
- **Task 2 (Medium):** "Cross-Lingual Intent." Detects Spanish text requiring active translation. (Target: Translate)
- **Task 3 (Hard):** "Sociolinguistic Nuance." Interprets Gen-Z slang ("mid", "no cap", "bounce") which standard dictionaries often fail to process correctly. (Target: Interpret)

### 2. The Reward Function
The environment uses a **deterministic grader** that provides a `1.0` reward for perfect intent alignment and `0.0` for failure. This creates a clear signal for Reinforcement Learning (RL) agents to learn the boundary between standard and non-standard text.

## 🚀 Technical Setup
### Local Execution
1. **Build Container:**
   ```bash
   docker build -t adaptive-comm-agent .