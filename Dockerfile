FROM python:3.12-alpine

WORKDIR /app

COPY docker-require.txt .

RUN pip install --no-cache-dir -r docker-require.txt

COPY config-replace.py .

CMD ["python", "config-replace.py"]
