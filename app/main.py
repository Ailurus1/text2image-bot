from launch import launch_bot
from utils import get_telegram_token, get_huggingface_token


def main() -> None:
    launch_bot(
        telegram_token=get_telegram_token(), 
        huggingface_token=get_huggingface_token()
    )


if __name__ == "__main__":
    main()
