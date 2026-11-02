import os
from hmac import compare_digest
from fastapi import Header, HTTPException

def verify_api_key(x_api_key: str | None = Header(default=None)):
    api_key = os.getenv("AIOS_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="API key not configured")
    if not x_api_key or not compare_digest(x_api_key, api_key):
        raise HTTPException(status_code=401, detail="Unauthorized")