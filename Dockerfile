FROM python:3.10-slim

WORKDIR /app

# Copy everything
COPY . .

# Install dependencies from the server folder
RUN pip install --no-cache-dir -r server/requirements.txt

# Expose the Hugging Face port
EXPOSE 7860

# Run the app using the module syntax to ensure main() is found
CMD ["python", "-m", "server.app"]
