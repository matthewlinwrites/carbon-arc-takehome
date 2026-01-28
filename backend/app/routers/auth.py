from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# Mock credentials for demo purposes
MOCK_USERNAME = "admin"
MOCK_PASSWORD = "password"
MOCK_TOKEN = "mock-jwt-token-12345"

# Auth dependency
security = HTTPBearer()


def require_auth(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Validate the Bearer token and return it if valid."""
    if credentials.credentials != MOCK_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return credentials.credentials


@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest) -> LoginResponse:
    if credentials.username != MOCK_USERNAME or credentials.password != MOCK_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return LoginResponse(token=MOCK_TOKEN, message="Login successful")
