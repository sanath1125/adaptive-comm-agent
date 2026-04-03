# Use Python 3.11 for stability
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn pydantic requests openai python-dotenv

# Expose the port Hugging Face expects
EXPOSE 7860

# Run the server using the module path
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
