from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()


def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to authenticate the current user via Bearer token.

    - Accepts token in `Authorization: Bearer <token>` header.
    - Validates against a fixed or environment-based mock token.
    - Raises 401 if token is missing or incorrect.

    Returns:
        A dict representing the authenticated user (e.g., {"username": "admin"}).
    """
    if token.credentials != "mocked-token":  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )
    return {"username": "admin"}