FROM python:3.10-slim

WORKDIR /app

# Copy requirements from the server folder
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything into the container
COPY . .

# Expose the Hugging Face port
EXPOSE 7860

# Run uvicorn pointing to the server folder
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
