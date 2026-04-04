---
title: Adaptive Comm Agent
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---
# Adaptive Communication AI Agent 🤖

This project is a submission for **Round 1**. It features an AI Agent capable of dynamically switching communication styles based on user input.

## 🚀 Overview
The system consists of a **Brain (Agent)** and a **Judge (Environment)**:
- **Agent:** Powered by `Llama-3.1-8B-Instruct` via the Hugging Face Inference Router.
- **Environment:** A FastAPI-based server that evaluates the Agent's decisions.

## 🧠 Decision Logic
The Agent classifies incoming messages into two categories:
1. **Action 0 (Standard):** Formal or standard English communication.
2. **Action 1 (Adaptive):** Foreign languages (e.g., Spanish) or modern Slang (e.g., "no cap", "mid").

## 🛠️ Technical Stack
- **Language:** Python 3.11
- **Framework:** FastAPI / Uvicorn
- **AI Model:** Meta Llama 3.1 8B
- **Deployment:** Dockerized container on Hugging Face Spaces

## ✅ Evaluation Results
- **Local Test Score:** 3.0/3.0
- **Test Cases:** Formal English (Pass), Spanish (Pass), Gen-Z Slang (Pass).
