import os
from fastapi import Header, HTTPException, status

def require_api_key(
    authorization: str | None = Header(default=None),
    x_api_key: str | None = Header(default=None),
):
    """
    Auth MVP : si PARLIOS_API_KEY n'est pas défini -> auth désactivée.
    Sinon, accepte Bearer <token> OU X-API-Key: <token>.
    """
    expected = os.getenv("PARLIOS_API_KEY")
    if not expected:
        return
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
    elif x_api_key:
        token = x_api_key
    if token != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid api key")
