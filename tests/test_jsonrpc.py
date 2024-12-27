import asyncio
import logging
import threading

import pytest
from pysignalbot.messages import Message


@pytest.mark.asyncio
async def test_getters(jsonrpc_bot, caplog):
    caplog.set_level(logging.DEBUG)

    events = {}

    @jsonrpc_bot.handler
    def on_message(number, msg: Message):
        logging.info(number, msg)

    accounts = jsonrpc_bot.get_accounts()
    for account in accounts:
        result = jsonrpc_bot.create_group(
            account,
            name="TEST_GROUP",
            description="TEST GENERATED",
            members=[],
        )
        group_id = result["id"]
        events[group_id] = threading.Event()

        jsonrpc_bot.send(account, msg="test", recipients=[group_id])
        await jsonrpc_bot.receive(account)
        result = jsonrpc_bot.quit_group(account, group_id)
        result = jsonrpc_bot.delete_group(account, group_id)

    for group_id in events:
        event: threading.Event = events[group_id]
        event.wait()
