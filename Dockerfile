FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir ckg-nvidia-nemoclaw

CMD ["ckg-nvidia-nemoclaw"]
