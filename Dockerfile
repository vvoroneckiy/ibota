FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/logs

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pycryptodome

COPY . .

CMD ["python", "bot.py"]
