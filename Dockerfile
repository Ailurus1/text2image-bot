FROM python:alpine3.17

ARG TG_TOKEN_ARG
ARG HF_TOKEN_ARG

ENV TG_TOKEN=$TG_TOKEN_ARG
ENV HF_TOKEN=$HF_TOKEN_ARG

COPY . .

RUN python3 -m pip install -r requirements.txt 

CMD [ "python3", "-u", "app/main.py" ]