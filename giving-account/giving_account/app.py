from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from giving_account.routers.google_auth.router import google_auth_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")
app.include_router(google_auth_router)
