FROM python:3.10-slim
WORKDIR /app
COPY . .
# Install the core requirements
RUN pip install --no-cache-dir -r server/requirements.txt
# Register the package
RUN pip install -e .
# THE PORT REQUIREMENT
EXPOSE 7860
# Run the formatted inference script
CMD ["python", "inference.py"]
