import os
from pysignalbot import Bot, Message
import asyncio

_SIGNAL_BOT_ENDPOINT = os.environ.get("SIGNAL_BOT_ENDPOINT", "localhost:8080")

signal_bot = Bot(_SIGNAL_BOT_ENDPOINT, mode=Bot.Mode.JSON_RPC)


@signal_bot.handler
def on_message(msg: Message):
    print(msg)


async def main():
    accounts = signal_bot.get_accounts()
    for account in accounts:
        await signal_bot.fetch(account)


if __name__ in {"__main__", "__mp_main__"}:
    asyncio.run(main())
