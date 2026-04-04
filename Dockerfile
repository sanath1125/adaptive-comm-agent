FROM python:3.11

WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Start the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
