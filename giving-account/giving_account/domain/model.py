import uuid
from typing import Optional, Union

import ulid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


def create_sequential_id():
    return ulid.new()


@dataclass
class BaseModel:
    id_: ulid.ULID = field(default_factory=create_sequential_id, init=False)
    created_at: datetime = field(default_factory=datetime.now, init=False)
    updated_at: datetime = field(default_factory=datetime.now, init=False)


class AccountProvider(str, Enum):
    GOOGLE = "google"


@dataclass
class AccountProfile(BaseModel):
    account_id: ulid.ULID
    nickname: str
    company: Optional[str] = field(default=None)
    avatar: Optional[str] = field(default=None)


@dataclass
class Account(BaseModel):
    email: str
    provider: Union[AccountProvider, str]
    profile: Optional[AccountProfile] = field(default=None)

    def update_profile(self, profile: AccountProfile):
        self.profile = profile
        self.updated_at = datetime.now()
