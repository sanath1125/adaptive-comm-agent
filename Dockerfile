FROM python:3.10-slim

WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r server/requirements.txt

# Open the port
EXPOSE 7860

# Run using the module path to satisfy the entry point check
CMD ["python", "-m", "server.app"]
