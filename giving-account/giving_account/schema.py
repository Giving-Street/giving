import uuid

from pydantic import BaseModel

from giving_account.domain.model import AccountProvider


class SignUpIn(BaseModel):
    email: str
    provider: AccountProvider


class SignUpOut(SignUpIn):
    id_: uuid.UUID
