import os
from pysignalbot import Bot
import asyncio
import logging

_SIGNAL_BOT_ENDPOINT = os.environ.get("SIGNAL_BOT_ENDPOINT", "localhost:8080")

signal_bot = Bot(_SIGNAL_BOT_ENDPOINT, mode=Bot.Mode.JSON_RPC)

@signal_bot.handler
def on_message(msg):
    logging.info(msg)

async def main():
    accounts = signal_bot.accounts()
    for account in accounts:
        await signal_bot.fetch(account)

if __name__ in {"__main__", "__mp_main__"}:
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
