"""
Some functions to get access tokens
for Telegram and HuggingFace from
specific environment variables or
check if they are not specified
"""
import os


def get_telegram_token() -> str:
    """
    Getting Telegram token
    (given by BotFather)
    from environment variable
    """
    tg_token = os.getenv("TG_TOKEN", "")
    if tg_token == "":
        raise RuntimeError(
            "Error: Token for Telegram is not specified!"
        )
    return tg_token


def get_huggingface_token() -> str:
    """
    Getting HuggingFace access token
    """
    hf_token = os.getenv("HF_TOKEN", "")
    if hf_token == "":
        raise RuntimeError(
            "Error: Token for HuggingFace is not specified!"
        )
    return hf_token
