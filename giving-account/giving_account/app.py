from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from giving_account.config import Config
from giving_account.routers.google_auth.router import google_auth_router

app = FastAPI()
app.state.config = Config()
app.add_middleware(SessionMiddleware, secret_key="!secret")
allows_origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allows_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.include_router(google_auth_router)
