import os
from pysignalapi import JsonRPCAPI, Message
import asyncio
import logging

_SIGNAL_API_ENDPOINT = os.environ.get("SIGNAL_API_ENDPOINT", "localhost:8080")

api = JsonRPCAPI(_SIGNAL_API_ENDPOINT)


@api.handler
def on_message(number, msg: Message):
    data = msg.envelope.dataMessage
    if data:
        logging.info(f"{number}: [{msg.envelope.sourceName}] {data.message}")
    else:
        logging.info(f"{number}: [{msg.envelope.sourceName}] envelope")


async def main():
    accounts = api.get_accounts()
    for account in accounts:
        await api.receive(account)
        # task = asyncio.create_task(api.receive(account))
        # asyncio.ensure_future(task)


if __name__ in {"__main__", "__mp_main__"}:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
