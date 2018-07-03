FROM python:alpine

RUN apk add --update --no-cache \
    git

WORKDIR /app

COPY requirements.txt /app
RUN pip install --user --no-cache-dir -r requirements.txt

COPY src /app

ENV PYTHONUNBUFFERED 1

CMD ["python", "monitor.py"]
