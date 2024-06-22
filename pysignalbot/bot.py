import enum
from .engine import JsonRPC, Native

class Bot:
    class Mode(enum.Enum):
        NATIVE = 0
        JSON_RPC = 1

    def __init__(self, url, mode: Mode = Mode.NATIVE):
        self._mode = mode
        self.message_handlers = []

        if self._mode == Bot.Mode.NATIVE:
            self.engine = Native(url)
        elif self._mode == Bot.Mode.JSON_RPC:
            self.engine = JsonRPC(url)
        else:
            raise RuntimeError(f"Unknown Signal mode: {self._mode}")

    def handler(self, func):
        self.message_handlers.append(func)

    async def fetch(self, number):
        if self._mode != Bot.Mode.JSON_RPC:
            raise RuntimeError("Listening allowed only in Json RPC mode")
        await self.engine.fetch(number, self.message_handlers)

    def accounts(self):
        result = self.engine.get("v1/accounts")
        return result.json()

    def device_add(self, phone_number):
        return self.engine.get(f"/v1/devices/{phone_number}", json={"uri": "string"})

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

    def account_remove(self, phone_number):
        return self.engine.delete(f"v1/accounts/{phone_number}/username")

    def add_device(self, phone_number):
        result = self.engine.post(
            f"v1/devices/{phone_number}",
            json={"uri": "string"},
        )
        return result.json()

    def get_groups(self, phone_number):
        result = self.engine.get(f"v1/groups/{phone_number}")
        return result.json()

    def send(self, phone_number, group, msg):
        result = self.engine.post(
            "v2/send",
            json={
                "number": phone_number,
                "message": msg,
                "recipients": [group],
            },
        )
        return result.json()
