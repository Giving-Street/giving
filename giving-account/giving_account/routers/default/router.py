from dataclasses import asdict
from typing import Optional

from fastapi import APIRouter, Depends, Request

from giving_account.domain.model import Account
from giving_account.routers.deps import get_user
from giving_account.schema import SignUpIn, SignUpOut

default_router = APIRouter()


@default_router.get("/accounts/{email}")
def get_account_from_email(email: str, user: Optional[dict] = Depends(get_user)):
    pass


@default_router.post("/accounts")
def signup(signup_in: SignUpIn, user: Optional[dict] = Depends(get_user)) -> SignUpOut:
    new_account = Account(email=signup_in.email, provider=signup_in.provider)
    return SignUpOut(**asdict(new_account))


@default_router.get("/me")
async def me(user: Optional[dict] = Depends(get_user)):
    return user
