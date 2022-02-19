from typing import Callable

from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, Request, status, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from giving_account.routers.deps import get_user, get_oauth
from authlib.integrations.starlette_client import OAuth

google_auth_router = APIRouter(prefix="/auth/google")


@google_auth_router.get("/login")
async def login(request: Request, get_oauth_: Callable[..., OAuth] = Depends(get_oauth)):
    try:
        user = await get_user(request=request)
        return RedirectResponse(url=request.app.state.config.front_url)
    except HTTPException:
        pass
    oauth = get_oauth_(request.app.state.config)
    redirect_uri = request.url_for('auth')
    redirect_response = await oauth.google.authorize_redirect(request, redirect_uri)
    return redirect_response


@google_auth_router.get('/auth')
async def auth(request: Request, get_oauth_: Callable[..., OAuth] = Depends(get_oauth)):
    oauth = get_oauth_(request.app.state.config)
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>', status_code=status.HTTP_401_UNAUTHORIZED)
    user = await oauth.google.parse_id_token(request, token)
    if user:
        request.session['google'] = {"user": dict(user)}
    return RedirectResponse(url=request.app.state.config.front_url)


@google_auth_router.get('/logout')
async def logout(request: Request):
    if not request.session.get("user"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User 정보가 없습니다")
    request.session.pop('user', None)
    return RedirectResponse(url='/')
