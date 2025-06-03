# filepath: d:\Study\BookTable-App\app\middleware\auth_middleware.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware

from app.auth.jwt_utils import verify_token


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.security = HTTPBearer()

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(("/docs", "/redocs", "/openapi.json")):
            return await call_next(request)

        if request.url.path in ["/api/login", "/api/register"]:
            return await call_next(request)

        if request.method == "OPTIONS":
            return await call_next(request)

        credentials: HTTPAuthorizationCredentials = await self.security(request)
        if credentials:
            token = credentials.credentials
            payload = verify_token(token)
            if payload is None:
                raise HTTPException(status_code=401, detail="Invalid or expired token")
            request.state.user = payload
        else:
            raise HTTPException(status_code=403, detail="Not authenticated")

        response = await call_next(request)
        return response

    # curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6InB1cnZhQGdtYWlsLmNvbSIsInJvbGUiOiJyZXN0YXVyYW50X21hbmFnZXIiLCJleHAiOjE3NDQ2Nzc3NjB9.1z4bfK-ksEBb0mVCYjALZo1ZogcMI7H6vgjOPPYPPBI" http://localhost:8000/your_protected_endpoint
