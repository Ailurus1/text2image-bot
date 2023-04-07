import os


def get_telegram_token() -> str:
    tg_token = os.getenv("TG_TOKEN", "")
    if tg_token == "":
        raise RuntimeError(
            "Error: Token for Telegram is not specified!"
        )
    return tg_token


def get_huggingface_token() -> str:
    hf_token = os.getenv("HF_TOKEN", "")
    if hf_token == "":
        raise RuntimeError(
            "Error: Token for HuggingFace is not specified!"
        )
    return hf_token
