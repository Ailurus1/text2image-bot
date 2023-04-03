from bot import Model, Bot
from consts import *

def main() -> None:
    model = Model()
    app = Bot(TG_TOKEN, model)
    app.run()

if __name__ == "__main__":
    main()
