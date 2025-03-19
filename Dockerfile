FROM python:3.11.10-slim


WORKDIR /usr/src/app

ARG MODEL=

ENV PORT=6666
ENV HOST=0.0.0.0

COPY $MODEL model
COPY server.py .
COPY common .

CMD python $HOST $PORT
