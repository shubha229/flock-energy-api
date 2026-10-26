
import requests

from app.config import settings


class PortalError(Exception):
    """Raised when a portal request fails."""

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class PortalAuthenticationError(PortalError):
    """Raised when portal authentication fails."""


class PortalClient:
    def __init__(self):
        self.base_url = settings.PORTAL_BASE_URL.rstrip("/")
        self.session = requests.Session()
        self.timeout = 15
        self.authenticated = False

    def login(self):
        if not settings.PORTAL_USERNAME or not settings.PORTAL_PASSWORD:
            raise PortalAuthenticationError(
                "Portal credentials are missing. Configure them in .env."
            )

        url = f"{self.base_url}/login"

        try:
            response = self.session.post(
                url,
                data={
                    "email": settings.PORTAL_USERNAME,
                    "password": settings.PORTAL_PASSWORD,
                },
                timeout=self.timeout,
                allow_redirects=False,
                headers={
                    "Accept": "application/json",
                    "Origin": self.base_url,
                    "Referer": f"{self.base_url}/login",
                    "X-Sveltekit-Action": "true",
                },
            )

            response.raise_for_status()
            result = response.json()

        except requests.RequestException as exc:
            raise PortalAuthenticationError(
                "Unable to complete the portal login request."
            ) from exc

        except ValueError as exc:
            raise PortalAuthenticationError(
                "Unable to parse the portal login response."
            ) from exc

        if (
            result.get("type") != "redirect"
            or result.get("status") != 303
            or result.get("location") != "/meters"
            or not self.session.cookies
        ):
            raise PortalAuthenticationError(
                "The portal login response did not match the expected "
                "successful login pattern."
            )

        self.authenticated = True

    def get(self, path, **kwargs):
        if not self.authenticated:
            self.login()

        url = f"{self.base_url}/{path.lstrip('/')}"

        try:
            response = self.session.get(
                url,
                timeout=self.timeout,
                **kwargs,
            )

            if response.status_code >= 400:
                raise PortalError(
                    f"Portal returned HTTP {response.status_code}.",
                    status_code=response.status_code,
                )

            return response

        except requests.Timeout as exc:
            raise PortalError(
                "The portal request timed out."
            ) from exc

        except requests.RequestException as exc:
            raise PortalError(
                "The portal request failed."
            ) from exc

    def close(self):
        self.session.close()
        self.authenticated = False
