FROM python:alpine3.17

COPY . .

RUN python3 -m pip install -r requirements.txt 

CMD [ "python3", "-u", "app/main.py" ]