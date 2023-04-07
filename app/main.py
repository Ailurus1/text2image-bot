from bot import Model, Bot
from tokens import *


def main() -> None:
    model = Model(get_huggingface_token())
    app = Bot(get_telegram_token(), model)
    app.run()


if __name__ == "__main__":
    main()
