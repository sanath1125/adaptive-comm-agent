FROM python:3.9
WORKDIR /code
# Change this line to point to the server folder:
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "inference.py"]
