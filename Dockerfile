FROM python:3.11.10-slim


WORKDIR /usr/src/app

ARG MODEL=

ENV PORT=6666
ENV HOST=0.0.0.0

COPY $MODEL model
COPY server.py .
COPY common .

RUN find . -name "requirements.txt" -exec cat {} \; >/usr/src/all_requirements.txt

RUN pip install -r /usr/src/all_requirements.txt

CMD python server.py $HOST $PORT
