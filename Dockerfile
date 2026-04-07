# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r server/requirements.txt

# Open the port Hugging Face expects
EXPOSE 7860

# Run the application
CMD ["python", "server/app.py"]
