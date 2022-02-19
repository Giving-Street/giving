from typing import Optional

from authlib.integrations.starlette_client import OAuth
from fastapi import Request, HTTPException
from starlette.config import Config

from giving_account.config import Config as GivingAccountConfig


async def get_user(request: Request) -> Optional[dict]:
    user = request.session.get('user')
    if not user:
        raise HTTPException(status_code=403, detail='Could not validate credentials.')

    return user


async def get_oauth():
    def _get_oauth(config: GivingAccountConfig) -> OAuth:
        config = Config(environ={
            "GOOGLE_CLIENT_ID": config.google_oauth.google_client_id,
            "GOOGLE_CLIENT_SECRET": config.google_oauth.google_client_secret
        })
        oauth = OAuth(config=config)
        conf_url = 'https://accounts.google.com/.well-known/openid-configuration'
        oauth.register(
            name='google',
            server_metadata_url=conf_url,
            client_kwargs={
                'scope': 'openid email profile'
            },
        )
        return oauth

    return _get_oauth