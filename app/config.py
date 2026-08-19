"""
Application configuration.

All BSE StAR MF (STARMF 2.0) connection details are supplied via environment
variables / a .env file so no secrets live in source control.
"""
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="STARMF_", extra="ignore", populate_by_name=True)

    # --- Database ------------------------------------------------------------------
    database_url: str = Field("postgresql+asyncpg://postgres:postgres@localhost:5432/starmf", alias="DATABASE_URL")

    # --- BSE StAR MF connection -------------------------------------------------
    protocol: str = "https"
    base_url: str = "www.example-starmf-host.com"  # set STARMF_BASE_URL in .env

    # --- Encryption headers (JOSE) ----------------------------------------------
    # Set STARMF_USE_ENCRYPTION=true to send/receive `Content-type: application/jose`
    # payloads instead of plain JSON. See app/security/jose.py for details and
    # caveats — BSE's exact JOSE profile (header params, key wrapping algorithm,
    # content encryption algorithm) is NOT published in the Postman collection
    # and must be confirmed against BSE's official StAR MF API documentation /
    # your onboarding pack before enabling this in production.
    use_encryption: bool = False
    api_org_id: str = ""  # X-API-Org-ID header, e.g. "member/0000:apikey..."

    # RSA key material for JOSE (PEM contents or file paths — see jose.py)
    member_private_key_path: Optional[str] = None   # used to SIGN outgoing requests
    bse_public_key_path: Optional[str] = None        # used to ENCRYPT outgoing requests
    member_private_key_for_decrypt_path: Optional[str] = None  # to DECRYPT responses
    bse_public_key_for_verify_path: Optional[str] = None        # to VERIFY response signature

    # --- HTTP behaviour -----------------------------------------------------------
    http_timeout_seconds: float = 30.0
    verify_tls: bool = True

    @property
    def root_url(self) -> str:
        return f"{self.protocol}://{self.base_url}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
