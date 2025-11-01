import os
from fastapi import Header, HTTPException

def require_api_key(x_api_key: str | None = Header(default=None)):
    expected = os.getenv("PARLIOS_API_KEY")
    if not expected:
        return  # pas d'auth si la variable n'est pas définie
    if x_api_key != expected:
        raise HTTPException(status_code=401, detail="invalid api key")
