from pydantic import BaseSettings, Field


class GoogleOAuthConfig(BaseSettings):
    google_client_id: str = Field(default="")
    google_client_secret: str = Field(default="")


class Config(BaseSettings):
    front_url: str = Field(default="http://localhost:3000")
    google_oauth: GoogleOAuthConfig = Field(default_factory=GoogleOAuthConfig)
