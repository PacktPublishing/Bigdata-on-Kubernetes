FROM python:3.11-alpine

RUN pip --no-cache-dir install fastapi uvicorn

EXPOSE 8087

COPY ./app /app

CMD uvicorn app.main:app --host 0.0.0.0 --port 8087
