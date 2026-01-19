from fastapi import HTTPException, Depends, Request, status
from stytch.core.response_base import StytchError

from app.core.stytch import stytch_client


class AuthUser:
    def __init__(self, user_id: str, org_id: str, org_permissions: list[str]):
        self.user_id = user_id
        self.org_id = org_id
        self.org_permissions = org_permissions

    def has_permission(self, permission: str) -> bool:
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


def _extract_bearer_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization") or ""
    scheme, _, token = auth_header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )
    return token


async def get_current_user(request: Request) -> AuthUser:
    session_jwt = _extract_bearer_token(request)

    try:
        auth_resp = stytch_client.sessions.authenticate(session_jwt=session_jwt)
    except StytchError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        ) from exc

    user_id = getattr(auth_resp, "member_id", None)
    org_id = getattr(auth_resp, "organization_id", None)

    # Try to pull permissions from the session JWT payload or custom claims.
    org_permissions: list[str] = []
    member_session = getattr(auth_resp, "member_session", None)
    if member_session:
        custom_claims = getattr(member_session, "custom_claims", {}) or {}
        org_permissions = (
            custom_claims.get("org_permissions")
            or custom_claims.get("permissions")
            or []
        )

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found"
        )

    if not org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No organization selected"
        )

    return AuthUser(user_id=user_id, org_id=org_id, org_permissions=org_permissions)

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