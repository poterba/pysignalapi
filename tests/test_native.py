import logging


def test_common(native_bot, caplog):
    caplog.set_level(logging.DEBUG)
    about = native_bot.about()
    logging.debug(about)
    configuration = native_bot.configuration()
    logging.debug(configuration)
    result = native_bot.set_configuration(logging_level="warn")
    logging.debug(result)


def test_getters(native_bot, caplog):
    caplog.set_level(logging.DEBUG)

    accounts = native_bot.get_accounts()
    for account in accounts:
        identities = native_bot.get_identities(account)
        for identity in identities:
            logging.info(identity)
        settings = native_bot.get_account_settings(account)
        print(settings)
        groups = native_bot.get_groups(account)
        for group in groups:
            members = native_bot.get_groups_members(account, group["id"])
            for member in members:
                logging.info(member)


def test_group(native_bot, caplog):
    caplog.set_level(logging.DEBUG)
    accounts = native_bot.get_accounts()
    for account in accounts:
        result = native_bot.create_group(
            account,
            name="TEST_GROUP",
            description="TEST GENERATED",
            members=[],
        )
        group_id = result["id"]
        native_bot.get_group(account, group_id)
        native_bot.update_group(
            account,
            group_id,
            base64_avatar=None,
            description="TEST UPDATED",
            name="TEST_GROUP+",
        )

        result = native_bot.quit_group(account, group_id)
        result = native_bot.delete_group(account, group_id)


# NOTE: some of identities have no number = no endpoint to trigger
# def test_identities(native_bot, caplog):
#     caplog.set_level(logging.DEBUG)
#     accounts = native_bot.get_accounts()
#     for account in accounts:
#         identities = native_bot.get_identities(account)
#         for identity in identities:
#             result = native_bot.trust_identity(
#                 account,
#                 numberToTrust=identity["number"],
#                 trust_all_or_safety_number=True,
#             )
#             print(result)


def test_profile(native_bot, caplog):
    caplog.set_level(logging.DEBUG)
    accounts = native_bot.get_accounts()
    for account in accounts:
        result = native_bot.update_profile(
            account,
            about="TEST UPDATED",
            base64_avatar=None,
            name="TEST ACCOUNT",
        )
        print(result)
