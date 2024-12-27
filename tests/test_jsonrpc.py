import logging
import threading

import pytest
from pysignalapi.messages import Message


@pytest.mark.asyncio
async def test_getters(jsonrpc_api, caplog):
    caplog.set_level(logging.DEBUG)

    events = {}

    @jsonrpc_api.handler
    def on_message(number, msg: Message):
        logging.info(number, msg)

    accounts = jsonrpc_api.get_accounts()
    for account in accounts:
        result = jsonrpc_api.create_group(
            account,
            name="TEST_GROUP",
            description="TEST GENERATED",
            members=[],
        )
        group_id = result["id"]
        events[group_id] = threading.Event()

        jsonrpc_api.send(account, msg="test", recipients=[group_id])
        await jsonrpc_api.receive(account)
        result = jsonrpc_api.quit_group(account, group_id)
        result = jsonrpc_api.delete_group(account, group_id)

    for group_id in events:
        event: threading.Event = events[group_id]
        event.wait()
