import logging


def test_common(native_api, caplog):
    caplog.set_level(logging.DEBUG)
    about = native_api.about()
    logging.debug(about)
    configuration = native_api.configuration()
    logging.debug(configuration)
    result = native_api.set_configuration(logging_level="warn")
    logging.debug(result)


def test_getters(native_api, caplog):
    caplog.set_level(logging.DEBUG)

    accounts = native_api.get_accounts()
    for account in accounts:
        identities = native_api.get_identities(account)
        for identity in identities:
            logging.info(identity)
        settings = native_api.get_account_settings(account)
        print(settings)
        groups = native_api.get_groups(account)
        for group in groups:
            members = native_api.get_groups_members(account, group["id"])
            for member in members:
                logging.info(member)


def test_group(native_api, caplog):
    caplog.set_level(logging.DEBUG)
    accounts = native_api.get_accounts()
    for account in accounts:
        result = native_api.create_group(
            account,
            name="TEST_GROUP",
            description="TEST GENERATED",
            members=[],
        )
        group_id = result["id"]
        native_api.get_group(account, group_id)
        native_api.update_group(
            account,
            group_id,
            base64_avatar=None,
            description="TEST UPDATED",
            name="TEST_GROUP+",
        )

        result = native_api.quit_group(account, group_id)
        result = native_api.block_group(account, group_id)
        result = native_api.delete_group(account, group_id)


# NOTE: some of identities have no number = no endpoint to trigger
# def test_identities(native_api, caplog):
#     caplog.set_level(logging.DEBUG)
#     accounts = native_api.get_accounts()
#     for account in accounts:
#         identities = native_api.get_identities(account)
#         for identity in identities:
#             result = native_api.trust_identity(
#                 account,
#                 numberToTrust=identity["number"],
#                 trust_all_or_safety_number=True,
#             )
#             print(result)


def test_profile(native_api, caplog):
    caplog.set_level(logging.DEBUG)
    accounts = native_api.get_accounts()
    for account in accounts:
        result = native_api.update_profile(
            account,
            about="TEST UPDATED",
            base64_avatar=None,
            name="TEST ACCOUNT",
        )
        print(result)
