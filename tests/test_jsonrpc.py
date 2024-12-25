import logging
from pysignalbot.messages import Message


async def test_getters(jsonrpc_bot, caplog):
    caplog.set_level(logging.DEBUG)

    @jsonrpc_bot.handler
    def on_message(msg: Message):
        logging.info(msg)

    accounts = jsonrpc_bot.get_accounts()
    for account in accounts:
        identities = jsonrpc_bot.get_identities(account)
        for identity in identities:
            logging.info(identity)
        groups = jsonrpc_bot.get_groups(account)
        for group in groups:
            members = jsonrpc_bot.get_groups_members(account, group["id"])
            for member in members:
                logging.info(member)

    accounts = jsonrpc_bot.get_accounts()
    for account in accounts:
        await jsonrpc_bot.receive(account)
