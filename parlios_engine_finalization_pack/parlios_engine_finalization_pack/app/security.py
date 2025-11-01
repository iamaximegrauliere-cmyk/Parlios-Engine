from fastapi import Header, HTTPException, status
import os

def require_api_key(authorization: str | None = Header(default=None)):
    expected = os.getenv("PARLIOS_API_KEY")
    if not expected:
        return  # security disabled if no key configured
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    if token != expected:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")