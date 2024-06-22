from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard
import uuid


@dataclass
class Mention:
    name: str
    number: str
    uuid: uuid.uuid4
    start: int
    length: int


@dataclass
class GroupInfo:
    groupId: str
    type: str


@dataclass
class DataMessage(JSONWizard):
    timestamp: int
    message: str
    expiresInSeconds: int
    viewOnce: bool
    groupInfo: GroupInfo
    mentions: list[Mention] = field(default_factory=list)


@dataclass
class Envelope:
    source: str
    sourceNumber: str | None
    sourceUuid: uuid.uuid4
    sourceName: str
    sourceDevice: int
    timestamp: int
    dataMessage: DataMessage


@dataclass
class Message(JSONWizard):
    account: str
    envelope: Envelope
