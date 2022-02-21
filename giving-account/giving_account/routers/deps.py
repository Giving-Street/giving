from typing import Optional

import jwt
from authlib.integrations.starlette_client import OAuth
from fastapi import Request, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from starlette.config import Config

from giving_account.config import Config as GivingAccountConfig

CREDENTIAL_ERROR = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials.")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/google/token")


async def get_config(request: Request):
    return request.app.state.config


async def get_current_user(
    token: str = Depends(oauth2_scheme), config: GivingAccountConfig = Depends(get_config)
) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            key=config.google_oauth.api_secret_key,
            algorithms=[config.google_oauth.algorithm],
            options={"verify_signature": False},
        )
    except jwt.PyJWTError as e:
        raise CREDENTIAL_ERROR

    email = payload.get("sub")
    if not email:
        raise CREDENTIAL_ERROR

    return email


async def get_google_oauth(request: Request):
    app_config = request.app.state.config
    if not isinstance(app_config, GivingAccountConfig):
        raise RuntimeError("Cannot get config")
    config = Config(
        environ={
            "GOOGLE_CLIENT_ID": app_config.google_oauth.google_client_id,
            "GOOGLE_CLIENT_SECRET": app_config.google_oauth.google_client_secret,
        }
    )
    oauth = OAuth(config=config)
    conf_url = "https://accounts.google.com/.well-known/openid-configuration"
    oauth.register(
        name="google",
        server_metadata_url=conf_url,
        client_kwargs={"scope": "openid email profile"},
    )
    return oauth
