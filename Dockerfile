FROM python:3.11.10-slim

WORKDIR /usr/src/app

ARG REQUIREMENTS_FILE=requirements.txt
ARG MODEL_NAME=main

ENV PORT=6666
ENV HOST="0.0.0.0"

COPY models/${MODEL_NAME}_model .
COPY ${REQUIREMENTS_FILE} ./requirements.txt
COPY common .
COPY server.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD python server.py $MODEL_NAME $HOST $PORT
