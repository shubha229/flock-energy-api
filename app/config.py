
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PORTAL_BASE_URL = os.getenv(
        "PORTAL_BASE_URL",
        "https://urja-ops.flockenergy.tech",
    ).rstrip("/")

    PORTAL_USERNAME = os.getenv("PORTAL_USERNAME", "")
    PORTAL_PASSWORD = os.getenv("PORTAL_PASSWORD", "")


settings = Settings()
