from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from main_app.config import settings


class FakeAccessTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request,
            call_next: RequestResponseEndpoint
    ) -> Response | JSONResponse:
        token = settings.ACCESS_TOKEN
        user_token = request.headers.get('Authorization')
        if user_token != token:
            return JSONResponse(content={'detail': 'sorry, you don\'t have the ~right~ access token'}, status_code=401)
        return await call_next(request)
