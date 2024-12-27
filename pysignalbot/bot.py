import asyncio
from typing import List
from . import engine, messages


class _BaseBot:
    def __init__(self, engine):
        self.engine = engine

    # API

    # Devices

    def qrcodelink(self, device_name="PYSIGNAL_DEVICE"):
        """returns png binary image"""
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

    def create_group(
        self,
        phone_number,
        *,
        name: str,
        description: str,
        members: list[str],
    ):
        result = self.engine.post(
            f"v1/groups/{phone_number}",
            json={
                "description": description,
                "expiration_time": 0,
                "group_link": "disabled",
                "members": members,
                "name": name,
                "permissions": {
                    "add_members": "only-admins",
                    "edit_group": "only-admins",
                },
            },
        )
        return result.json()

    def get_group(self, phone_number, group_id: str):
        result = self.engine.get(f"v1/groups/{phone_number}/{group_id}")
        return result.json()

    def update_group(
        self,
        phone_number,
        group_id: str,
        *,
        base64_avatar: str,
        description: str,
        name: str,
        expiration_time: int = 0,
    ):
        result = self.engine.put(
            f"v1/groups/{phone_number}/{group_id}",
            json={
                "base64_avatar": base64_avatar,
                "description": description,
                "expiration_time": expiration_time,
                "name": name,
            },
        )
        return result.text

    def delete_group(self, phone_number, group_id: str):
        result = self.engine.delete(f"v1/groups/{phone_number}/{group_id}")
        return result.text

    def quit_group(self, phone_number, group_id: str):
        result = self.engine.post(f"v1/groups/{phone_number}/{group_id}/quit")
        return result.text

    def get_groups_members(self, phone_number, group_id):
        result = self.engine.get(f"v1/groups/{phone_number}/{group_id}")
        return result.json()

    # Messages

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

    # Profiles

    def update_profile(
        self,
        phone_number,
        about,
        base64_avatar,
        name,
    ):
        result = self.engine.put(
            f"/v1/profiles/{phone_number}",
            json={"about": about, "base64_avatar": base64_avatar, "name": name},
        )
        return result.text

    # Identities

    def get_identities(self, phone_number):
        result = self.engine.get(f"v1/identities/{phone_number}")
        return result.json()

    def trust_identity(
        self,
        phone_number,
        *,
        numberToTrust: str,
        trust_all_or_safety_number: bool | str,
    ):
        data = {}
        if isinstance(trust_all_or_safety_number, bool):
            data["trust_all_known_keys"] = trust_all_or_safety_number
        elif isinstance(trust_all_or_safety_number, str):
            data["verified_safety_number"] = trust_all_or_safety_number
        else:
            raise RuntimeError("Set `trust_all_or_safety_number` as bool or string!")

        result = self.engine.put(
            f"/v1/identities/{phone_number}/trust/{numberToTrust}",
            json=data,
        )
        return result.text


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
        async with self.engine.fetch(number) as message:
            for handler in self.message_handlers:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(message)
                    else:
                        handler(message)
                except:  # noqa: E722
                    pass
