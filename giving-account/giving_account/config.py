import secrets

from pydantic import BaseSettings, Field


class GoogleOAuthConfig(BaseSettings):
    google_client_id: str = Field(default="")
    google_client_secret: str = Field(default="")
    api_secret_key: str = Field(default_factory=secrets.token_urlsafe)
    algorithm: str = Field(default="HS256")
    expiration_in_minutes: int = Field(default=30)


class Config(BaseSettings):
    front_url: str = Field(default="http://localhost:3000")
    google_oauth: GoogleOAuthConfig = Field(default_factory=GoogleOAuthConfig)
