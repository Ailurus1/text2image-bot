# Text2image-bot
The simpliest possible implementation of telegram bot using `python-telegram-bot` and `HuggingFace Inference API`

## How to run
First of all you have to generate token with Telegram BotFather and user access token from HuggingFace.
After you successfully create it you can just put them to local `.env` file and then just run docker build and run:

```bash

docker build -t text2image-bot:latest .

docker run --env-file=.env -it text2image-bot:latest
```
