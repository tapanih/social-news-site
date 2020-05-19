FROM python:3.8-alpine
WORKDIR /app

COPY ./requirements.txt ./
RUN apk add --no-cache gcc libffi-dev \
    openssl-dev musl-dev postgresql-dev && \
    pip install -r requirements.txt
COPY . .

RUN adduser -D appuser && chown -R appuser /app
USER appuser

CMD gunicorn --preload --workers 1 --bind 0.0.0.0:$PORT application:app