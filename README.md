# pysignalbot

Simple yet powerful library to work with [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api). It supports both sync and async modes of origin Docker container, providing supplying API.

```python
import asyncio
from pysignalbot import Bot

bot = Bot("localhost:8080", mode=Bot.Mode.JSON_RPC)

@bot.handler
def on_message(msg):
    logging.info(msg)

async def main():
    accounts = bot.accounts()
    for account in accounts:
        await bot.fetch(account)

if __name__ in {"__main__", "__mp_main__"}:
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
```

## Credits:

This project is heavily inspired by:

- [signalbot](https://github.com/filipre/signalbot)
- [pysignalclirestapi](https://github.com/bbernhard/pysignalclirestapi)
