import io
import os
import pytest
from pysignalapi import NativeAPI, JsonRPCAPI
from PIL import Image

_SIGNAL_API_ENDPOINT = os.getenv("SIGNAL_API_ENDPOINT", "localhost:8080")
_SIGNAL_API_CREATE = os.getenv("SIGNAL_API_CREATE", True)


@pytest.fixture(scope="session")
def native_api():
    api = NativeAPI(_SIGNAL_API_ENDPOINT)
    accounts = api.get_accounts()
    if not accounts:
        if _SIGNAL_API_CREATE:
            image = api.qrcodelink("PYSIGNAL_API_TEST")
            Image.open(io.BytesIO(image)).show()
        raise RuntimeError("No linked accounts")
    return api


@pytest.fixture(scope="session")
def jsonrpc_api():
    api = JsonRPCAPI(_SIGNAL_API_ENDPOINT)
    accounts = api.get_accounts()
    if not accounts:
        if _SIGNAL_API_CREATE:
            image = api.qrcodelink("PYSIGNAL_API_TEST")
            Image.open(io.BytesIO(image)).show()
        raise RuntimeError("No linked accounts")
    return api
