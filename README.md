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
