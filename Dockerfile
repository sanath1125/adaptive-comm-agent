FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r server/requirements.txt
# This ensures the 'server' package is recognized
RUN pip install -e .
EXPOSE 7860
# Use the module flag to start
CMD ["python", "-m", "server.app"]
