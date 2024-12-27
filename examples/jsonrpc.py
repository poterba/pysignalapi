import os
from pysignalbot import JsonRPCBot, Message
import asyncio
import logging

_SIGNAL_BOT_ENDPOINT = os.environ.get("SIGNAL_BOT_ENDPOINT", "localhost:8080")

signal_bot = JsonRPCBot(_SIGNAL_BOT_ENDPOINT)


@signal_bot.handler
def on_message(number, msg: Message):
    data = msg.envelope.dataMessage
    if data:
        logging.info(f"{number}: [{msg.envelope.sourceName}] {data.message}")
    else:
        logging.info(f"{number}: [{msg.envelope.sourceName}] envelope")


async def main():
    accounts = signal_bot.get_accounts()
    for account in accounts:
        await signal_bot.receive(account)
        # task = asyncio.create_task(signal_bot.receive(account))
        # asyncio.ensure_future(task)


if __name__ in {"__main__", "__mp_main__"}:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
