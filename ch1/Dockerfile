FROM alpine

RUN apk add --no-cache python3 py3-pip

RUN pip3 install fastapi uvicorn

EXPOSE 8087

COPY ./app /app

CMD uvicorn app.main:app --host 0.0.0.0 --port 8087
