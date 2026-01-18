import httpx
from fastapi import HTTPException, Depends, Request, status
from clerk_backend_api.security import AuthenticationRequestOptions
from app.core.clerk import clerk
from app.core.config import settings

#frontend (jwt token from clerk) -> backend
#backend authenticates the token
#gets user details from clerk
#check user permissions