import logging


def test_getters(native_bot, caplog):
    caplog.set_level(logging.DEBUG)
    accounts = native_bot.get_accounts()
    for account in accounts:
        identities = native_bot.get_identities(account)
        for identity in identities:
            logging.info(identity)
        groups = native_bot.get_groups(account)
        for group in groups:
            members = native_bot.get_groups_members(account, group["id"])
            for member in members:
                logging.info(member)
