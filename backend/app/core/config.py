import os
from  dotenv import load_dotenv

load_dotenv()

class Config:
    STYTCH_PROJECT_ID: str = os.getenv("STYTCH_PROJECT_ID", "")
    STYTCH_SECRET: str = os.getenv("STYTCH_SECRET", "")
    STYTCH_ENVIRONMENT: str = os.getenv("STYTCH_ENVIRONMENT", "test")
    STYTCH_PUBLIC_TOKEN: str = os.getenv("STYTCH_PUBLIC_TOKEN", "")


    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "")

    FREE_TIER_MEMBERSHIP_LIMIT: int = 2
    PRO_TIER_MEMBERSHIP_LIMIT: int = 0

settings = Config()