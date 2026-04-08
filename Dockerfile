FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies from your server requirements
RUN pip install --no-cache-dir -r server/requirements.txt

# Install your local package in editable mode as requested
RUN pip install -e .

# REQUIRED: The port for Hugging Face Spaces communication
EXPOSE 7860

# Run the inference script
CMD ["python", "inference.py"]
