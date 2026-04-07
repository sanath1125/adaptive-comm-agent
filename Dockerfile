FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r server/requirements.txt
EXPOSE 7860
# Running as a module ensures server.app is in the python path
CMD ["python", "-m", "server.app"]
