from typing import List
from . import engine, messages


class _BaseBot:

    def __init__(self, engine):
        self.engine = engine

    # API

    # retval: png binary image
    def qrcodelink(self, device_name="PYSIGNAL_DEVICE"):
        result = self.engine.get(f"v1/qrcodelink?device_name={device_name}")
        return result.content

    def register(self, phone_number, use_voice=False):
        result = self.engine.post(
            f"v1/register/{phone_number}",
            json={"captcha": "string", "use_voice": use_voice},
        )
        return result.content

    def unregister(self, phone_number):
        result = self.engine.post(
            f"v1/unregister/{phone_number}",
            json={"delete_account": False, "delete_local_data": True},
        )
        return result.content

    # accounts

    def get_accounts(self):
        result = self.engine.get("v1/accounts")
        return result.json()

    def username_remove(self, phone_number):
        return self.engine.delete(f"v1/accounts/{phone_number}/username")

    # groups

    def get_groups(self, phone_number):
        result = self.engine.get(f"v1/groups/{phone_number}")
        return result.json()

    def get_groups_members(self, phone_number, group_id):
        result = self.engine.get(f"v1/groups/{phone_number}/{group_id}")
        return result.json()

    # messages

    def send(
        self,
        phone_number,
        msg,
        recipients: List[str],
        mentions: List[messages.SendMention] = [],
        styled=False,
    ):
        result = self.engine.post(
            "v2/send",
            json={
                "number": phone_number,
                "message": msg,
                "recipients": recipients,
                "mentions": mentions,
                "text_mode": "styled" if styled else "normal",
            },
        )
        return result.json()

    # Identities


class NativeBot(_BaseBot):
    def __init__(self, url):
        super().__init__(engine.NativeEngine(url))

    def receive(self, phone_number):
        result = self.engine.get(f"v1/receive/{phone_number}")
        return result.json()


class JsonRPCBot(_BaseBot):
    def __init__(self, url):
        super().__init__(engine.JsonRPCEngine(url))
        self.message_handlers = []

    def handler(self, func):
        self.message_handlers.append(func)

    async def receive(self, number):
        await self.engine.fetch(number, self.message_handlers)
