FROM python:3.10-slim

# 1. Set working directory
WORKDIR /app

# 2. Install essential system dependencies (prevents many connection errors)
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 3. Copy files
COPY . .

# 4. Install dependencies
RUN pip install --no-cache-dir -r server/requirements.txt
RUN pip install -e .

# 5. REQUIRED: Hugging Face default port
EXPOSE 7860

# 6. Run the script
CMD ["python", "inference.py"]
