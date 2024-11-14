FROM python:3.11.10-slim

WORKDIR /usr/src/app

ARG REQUIREMENTS_FILE=requirements.txt
ARG MODEL_NAME=main

ENV PORT=6666
ENV HOST="0.0.0.0"
ENV MODEL_NAME=${MODEL_NAME}

COPY models/${MODEL_NAME}_model ${MODEL_NAME}_model
COPY common common
COPY server.py .
COPY ${REQUIREMENTS_FILE} ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD python server.py $MODEL_NAME $HOST $PORT
