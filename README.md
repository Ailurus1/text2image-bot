# Text2image-bot
The simpliest possible implementation of telegram bot using `python-telegram-bot` and `HuggingFace Inference API`

## How to run
First of all you have to generate token with Telegram BotFather and user access token from HuggingFace.
After you successfully create it you can just put them to environment variables `TG_TOKEN` and `HF_TOKEN` and then just run docker build and run:

```bash
export TG_TOKEN=<your telegram token>
export HF_TOKEN=<your huggingface token>

docker build \
    --build-arg TG_TOKEN_ARG=$TG_TOKEN \
    --build-arg HF_TOKEN_ARG=$HF_TOKEN \
    -t text2image-bot:latest .

docker run text2image-bot:latest
```

or in both cases you can simply run `scripts/build_run.sh`

---
#### Dockerfile Description
>`FROM python:alpine3.17`

We use lightweight `Alpine` distribution with Python 3.9 for optimal size of built image.

>`ARG TG_TOKEN_ARG`
>`ARG HF_TOKEN_ARG`
>
>`ENV TG_TOKEN=$TG_TOKEN_ARG`
>`ENV HF_TOKEN=$HF_TOKEN_ARG`

There are two build arguments for Telegram and HuggingFace tokens which then become values of relevant environment variables inside building container.

>`COPY . .`
>
>`RUN python3 -m pip install -r requirements.txt `

Then we just copy needed files (see `.dockerignore`) of repository inside container and run installation of Python dependencies specified in `requirements.txt`.

>`CMD [ "python3", "-u", "app/main.py" ]`

Finally run `main.py` script to deploy bot inside container with `-u` option to see stdout while running.
