FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r server/requirements.txt
RUN pip install -e .
EXPOSE 7860
CMD ["python", "-m", "server.app"]
