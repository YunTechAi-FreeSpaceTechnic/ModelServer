FROM python:3.11.10-slim

WORKDIR /usr/src/app

ARG REQUIREMENTS_FILE=requirements.txt
ENV APP_NAME=main
ENV APP_PATH=main
ENV PORT=6666
ENV HOST="0.0.0.0"

COPY ${REQUIREMENTS_FILE} ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD python server.py $MODEL_NAME $HOST $PORT
