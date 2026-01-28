from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# Mock credentials for demo purposes
MOCK_USERNAME = "admin"
MOCK_PASSWORD = "password"
MOCK_TOKEN = "mock-jwt-token-12345"
AUTH_COOKIE_NAME = "auth_token"

# Auth dependency
security = HTTPBearer(auto_error=False)


def require_auth(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    """Validate auth via Bearer token header OR cookie and return token if valid."""
    token = credentials.credentials if credentials else request.cookies.get(AUTH_COOKIE_NAME)
    if not token:
        # Preserve FastAPI HTTPBearer default behavior for missing auth
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")

    if token != MOCK_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return token


@router.get("/login", response_class=HTMLResponse)
def login_page(next: str = "/tasks") -> HTMLResponse:
    """Simple browser login form that sets an auth cookie via /auth/session."""
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Login</title>
    <style>
      body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 40px; }}
      form {{ max-width: 420px; display: grid; gap: 12px; }}
      label {{ display: grid; gap: 6px; font-weight: 600; }}
      input {{ padding: 10px 12px; font-size: 14px; }}
      button {{ padding: 10px 12px; font-size: 14px; cursor: pointer; }}
      .hint {{ color: #555; font-size: 13px; }}
      code {{ background: #f6f8fa; padding: 2px 6px; border-radius: 6px; }}
    </style>
  </head>
  <body>
    <h2>Task API Login</h2>
    <p class="hint">Use <code>admin</code> / <code>password</code>. After login you’ll be redirected to <code>{next}</code>.</p>
    <form method="post" action="/auth/session">
      <input type="hidden" name="next" value="{next}" />
      <label>
        Username
        <input name="username" autocomplete="username" required />
      </label>
      <label>
        Password
        <input type="password" name="password" autocomplete="current-password" required />
      </label>
      <button type="submit">Log in</button>
    </form>
  </body>
</html>
"""
    return HTMLResponse(content=html)


@router.post("/session")
async def create_session(request: Request) -> RedirectResponse:
    """Create a browser session by setting an HttpOnly auth cookie.

    This intentionally avoids FastAPI's Form(...) dependency so we don't require
    the optional "python-multipart" package.
    """
    content_type = (request.headers.get("content-type") or "").lower()
    username = ""
    password = ""
    next_url = "/tasks"

    if "application/json" in content_type:
        data = await request.json()
        username = str(data.get("username") or "")
        password = str(data.get("password") or "")
        next_url = str(data.get("next") or next_url)
    else:
        body = (await request.body()).decode("utf-8", errors="ignore")
        form = parse_qs(body)
        username = (form.get("username") or [""])[0]
        password = (form.get("password") or [""])[0]
        next_url = (form.get("next") or [next_url])[0]

    if username != MOCK_USERNAME or password != MOCK_PASSWORD:
        # Keep this simple for now; browser will show plain error text.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    response = RedirectResponse(url=next_url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=MOCK_TOKEN,
        httponly=True,
        samesite="lax",
        path="/",
    )
    return response


@router.get("/logout")
def logout(next: str = "/auth/login") -> RedirectResponse:
    """Clear the auth cookie for browser usage."""
    response = RedirectResponse(url=next, status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key=AUTH_COOKIE_NAME, path="/")
    return response


@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest) -> LoginResponse:
    if credentials.username != MOCK_USERNAME or credentials.password != MOCK_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return LoginResponse(token=MOCK_TOKEN, message="Login successful")
