from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth

google_auth_router = APIRouter(prefix="/auth/google")


@google_auth_router.on_event("startup")
async def startup():
    from giving_account.app import app
    config = Config(environ={
        "GOOGLE_CLIENT_ID": app.state.config.google_oauth.google_client_id,
        "GOOGLE_CLIENT_SECRET": app.state.config.google_oauth.google_client_secret
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
    app.state.google_oauth = oauth


@google_auth_router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    redirect_response = await request.app.state.google_oauth.google.authorize_redirect(request, redirect_uri)
    return redirect_response


@google_auth_router.get('/auth')
async def auth(request: Request):
    try:
        token = await request.app.state.google_oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>', status_code=status.HTTP_401_UNAUTHORIZED)
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url=request.app.state.config.front_url)


@google_auth_router.get('/logout')
async def logout(request: Request):
    if not request.session.get("user"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User 정보가 없습니다")
    request.session.pop('user', None)
    return RedirectResponse(url='/')
