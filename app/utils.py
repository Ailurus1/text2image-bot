import os
import time

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


def retry(num_retries: int, wait_time: int):
    """
    A decorator for automatic retry
    when got empty result from HF
    or when any exception occured
    """
    def _outer_wrapper(func):
        def _inner_wrapper(*args, **kwargs):
            for _ in range(num_retries):
                try:
                    result = func(*args, **kwargs)
                except:
                    time.sleep(wait_time)
                else:
                    if result is not None:
                        return result
        return _inner_wrapper
    return _outer_wrapper