from bot import Model, Bot
from consts import *

def main() -> None:
    app = Bot(TOKEN, Model())
    app.run()

if __name__ == "__main__":
    main()
