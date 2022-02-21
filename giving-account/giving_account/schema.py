import uuid

import ulid
from pydantic import BaseModel

from giving_account.domain.model import AccountProvider


def stringify_ulid(ulid_id: ulid.ULID):
    return ulid_id.str


class BaseSchema(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ulid.ULID: stringify_ulid}


class SignUpIn(BaseSchema):
    email: str
    provider: AccountProvider


class SignUpOut(BaseSchema):
    id_: ulid.ULID
