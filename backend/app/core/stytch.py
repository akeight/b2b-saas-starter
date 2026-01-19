from stytch import B2BClient

from app.core.config import settings


def _resolve_environment(env_name: str) -> str:
    """Normalize environment to values accepted by Stytch ('test' or 'live')."""
    normalized = (env_name or "").strip().lower()
    return "live" if normalized == "live" else "test"


stytch_client = B2BClient(
    project_id=settings.STYTCH_PROJECT_ID,
    secret=settings.STYTCH_SECRET,
    environment=_resolve_environment(settings.STYTCH_ENVIRONMENT),
)