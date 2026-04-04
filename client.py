import os
from huggingface_hub import InferenceClient

def perform_inference(message: str):
    # Retrieve token from environment variables
    token = os.getenv("HF_TOKEN")
    
    # Initialize client
    client = InferenceClient(api_key=token)
    
    # Simple logic: If 'translate' is in the message, we suggest Action 1
    action = 1 if "translate" in message.lower() else 0
    
    # Call the model (Llama 3.1)
    try:
        response = client.chat_completion(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[{"role": "user", "content": message}],
            max_tokens=100
        )
        text_content = response.choices[0].message.content
    except Exception as e:
        text_content = f"Error calling model: {str(e)}"

    return {
        "response": text_content,
        "action": action
    }
