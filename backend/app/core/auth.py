import httpx
from fastapi import HTTPException, Depends, Request, status
from clerk_backend_api.security import AuthenticationRequestOptions
from app.core.clerk import clerk
from app.core.config import settings

#frontend (jwt token from clerk) -> backend
#backend authenticates the token
#gets user details from clerk
#check user permissions

class AuthUser:
    def __init__(self, user_id: str, org_id: str, org_permissions: list[str]):
        self.user_id = user_id
        self.org_id = org_id
        self.org_persissions = org_permissions

    def has_permissions(self, permission: str) -> bool:
        return permission in self.org_permissions

    @property
    def can_view(self) -> bool:
        return self.has_permission("org:tasks:view")

    @property
    def can_create(self) -> bool:
        return self.has_permission("org:tasks:create")

    @property
    def can_edit(self) -> bool:
        return self.has_permission("org:tasks:edit")

    @property
    def can_delete(self) -> bool:
        return self.has_permission("org:tasks:delete")

def convert_to_httpx_request(fastapi_request: Request) -> httpx.Request:
    return httpx.Request(
        method=fastapi_request.method,
        url=str(fastapi_request.url),
        headers=dict(fastapi_request.headers)
    )

async def get_current_user(request: Request) -> AuthUser:
    httpx_request = convert_to_httpx_request(request)

    request_state = clerk.authenticate_request(
        httpx_request,
        AuthenticationRequestOptions(
            authorized_parties=[settings.FRONTEND_URL]
        )
    )   

    if not request_state.is_signed_in:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    claims = request_state.payload
    user_id = claims.get("sub")
    org_id = claims.get("org_id")
    org_permissions = claims.get("org_permissions", []) or claims.get("permissions", []) or []

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found")

    if not org_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No organization selected")

    return AuthUser(user_id=user_id, org_id=org_id, org_persissions=org_permissions)

def require_view(user: AuthUser = Depends(get_current_user)) -> AuthUser:
    if not user.can_view:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view")
    return user

def require_create(user: AuthUser = Depends(get_current_user)) -> AuthUser:
    if not user.can_create:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create")
    return user

def require_edit(user: AuthUser = Depends(get_current_user)) -> AuthUser:
    if not user.can_edit:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to edit")
    return user

def require_delete(user: AuthUser = Depends(get_current_user)) -> AuthUser:
    if not user.can_delete:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete")
    return user