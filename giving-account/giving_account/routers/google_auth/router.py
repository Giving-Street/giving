from datetime import datetime, timedelta
from typing import Optional

import jwt
from authlib.integrations.base_client import OAuthError
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request, status, HTTPException, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse

from giving_account.config import Config
from giving_account.routers.deps import get_current_user, get_google_oauth, get_config

google_auth_router = APIRouter(prefix="/auth/google")


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
    secret_key: Optional[str] = None,
    algorithm: Optional[str] = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


@google_auth_router.get("/login")
async def login(request: Request, oauth: OAuth = Depends(get_google_oauth), config: Config = Depends(get_config)):
    try:
        user = await get_current_user(config=config)
        return RedirectResponse(url=config.front_url)
    except HTTPException:
        pass
    redirect_uri = request.url_for("auth")
    redirect_response = await oauth.google.authorize_redirect(request, redirect_uri)
    return redirect_response


@google_auth_router.get("/token")
async def auth(request: Request, oauth: OAuth = Depends(get_google_oauth), config: Config = Depends(get_config)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f"<h1>{error.error}</h1>", status_code=status.HTTP_401_UNAUTHORIZED)
    user = await oauth.google.parse_id_token(request, token)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user information")

    access_token = create_access_token(
        data={"sub": user["email"], "alg": config.google_oauth.algorithm},
        expires_delta=timedelta(config.google_oauth.expiration_in_minutes),
    )

    response = RedirectResponse(config.front_url)
    response.set_cookie("Authorization", f"Bearer {access_token}")
    return response


@google_auth_router.get("/logout")
async def logout(request: Request, config: Config = Depends(get_config)):
    request.cookies.pop("Authorization")
    return RedirectResponse(url=config.front_url)
