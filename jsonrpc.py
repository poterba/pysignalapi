import os
from pysignalbot import JsonRPCBot, Message
import asyncio
import logging

_SIGNAL_BOT_ENDPOINT = os.environ.get("SIGNAL_BOT_ENDPOINT", "localhost:8080")

signal_bot = JsonRPCBot(_SIGNAL_BOT_ENDPOINT)


@signal_bot.handler
def on_message(msg: Message):
    logging.info(msg)


async def main():
    accounts = signal_bot.get_accounts()
    for account in accounts:
        await signal_bot.receive(account)


if __name__ in {"__main__", "__mp_main__"}:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
