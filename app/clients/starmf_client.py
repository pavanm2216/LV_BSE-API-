"""
Thin async client around BSE STARMF 2.0 REST API.
"""
from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.security import jose


def _extract_html_hint(html: str) -> str:
    """Extract a readable message from BSE's HTML error pages."""
    # Try #mainTitleAlign element
    m = re.search(r'id=["\']mainTitleAlign["\'][^>]*>(.*?)</td>', html, re.S)
    if m:
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if text:
            return text[:300]
    # Try <title>
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.S | re.I)
    if m:
        text = m.group(1).strip()
        if text:
            return text[:300]
    # Fallback: strip all tags
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:300]


class StarMFClient:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._token: Optional[str] = None
        self._client = httpx.AsyncClient(
            timeout=settings.http_timeout_seconds,
            verify=settings.verify_tls,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    @property
    def token(self) -> Optional[str]:
        return self._token

    def set_token(self, token: str) -> None:
        self._token = token

    # -- core request plumbing ---------------------------------------------------

    def _headers(self, *, authed: bool) -> dict:
        headers = {"Accept": "application/json"}
        if self._settings.use_encryption:
            headers["Content-type"] = "application/jose"
            if self._settings.api_org_id:
                headers["X-API-Org-ID"] = self._settings.api_org_id
        else:
            headers["Content-Type"] = "application/json"

        if authed:
            if not self._token:
                raise HTTPException(status_code=401, detail="Not logged in to STARMF. Call /login first.")
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def _build_body(self, data: dict) -> Any:
        envelope = {"data": data}
        if self._settings.use_encryption:
            if not (self._settings.member_private_key_path and self._settings.bse_public_key_path):
                raise HTTPException(
                    status_code=500,
                    detail="STARMF_USE_ENCRYPTION is true"" but signing/encryption keys are not configured.",
                )
            return jose.sign_and_encrypt(
                envelope,
                sign_key_path=self._settings.member_private_key_path,
                encrypt_key_path=self._settings.bse_public_key_path,
            )
        return envelope

    def _parse_response(self, response: httpx.Response) -> dict:
        if self._settings.use_encryption and "application/jose" in response.headers.get("content-type", ""):
            if not (
                self._settings.member_private_key_for_decrypt_path
                and self._settings.bse_public_key_for_verify_path
            ):
                raise HTTPException(
                    status_code=500,
                    detail="Received an encrypted response but decrypt/verify keys are not configured.",
                )
            return jose.decrypt_and_verify(
                response.text,
                decrypt_key_path=self._settings.member_private_key_for_decrypt_path,
                verify_key_path=self._settings.bse_public_key_for_verify_path,
            )
        try:
            return response.json()
        except ValueError:
            hint = _extract_html_hint(response.text)
            raise HTTPException(status_code=502, detail={
                "error": "Non-JSON response from STARMF",
                "bse_status_code": response.status_code,
                "likely_cause": "IP not whitelisted / session expired / BSE maintenance",
                "page_hint": hint,
                "raw_snippet": response.text[:300],
            })

    async def _log(self, db: AsyncSession | None, *, endpoint: str, status_code: int,
                   response_status: str, error_code: str | None, error_message: str | None,
                   request_ts: datetime, response_ts: datetime) -> None:
        if db is None:
            return
        from app.db.models import BseApiLog
        duration = int((response_ts - request_ts).total_seconds() * 1000)
        db.add(BseApiLog(
            id=uuid.uuid4(),
            endpoint=endpoint,
            http_method="POST",
            bse_status_code=status_code,
            response_status=response_status,
            error_code=error_code,
            error_message=error_message,
            request_timestamp=request_ts,
            response_timestamp=response_ts,
            duration_ms=duration,
        ))
        await db.commit()

    async def post(self, path: str, data: dict, *, authed: bool = True, db: AsyncSession | None = None) -> dict:
        url = f"{self._settings.root_url}/{path.lstrip('/')}"
        headers = self._headers(authed=authed)
        body = self._build_body(data)
        request_ts = datetime.now(timezone.utc)

        try:
            if isinstance(body, str):
                response = await self._client.post(url, content=body, headers=headers)
            else:
                response = await self._client.post(url, json=body, headers=headers)
        except httpx.RequestError as exc:
            response_ts = datetime.now(timezone.utc)
            await self._log(db, endpoint=path, status_code=502, response_status="failed",
                            error_code="request_error", error_message=str(exc),
                            request_ts=request_ts, response_ts=response_ts)
            raise HTTPException(status_code=502, detail=f"Could not reach STARMF host: {exc}") from exc

        response_ts = datetime.now(timezone.utc)
        try:
            parsed = self._parse_response(response)
        except HTTPException as exc:
            await self._log(db, endpoint=path, status_code=response.status_code,
                            response_status="failed", error_code="non_json",
                            error_message=str(exc.detail)[:500],
                            request_ts=request_ts, response_ts=response_ts)
            raise

        await self._log(
            db, endpoint=path, status_code=response.status_code,
            response_status="success" if response.status_code < 400 else "failed",
            error_code=None if response.status_code < 400 else str(response.status_code),
            error_message=None if response.status_code < 400 else str(parsed)[:500],
            request_ts=request_ts, response_ts=response_ts,
        )

        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=parsed)

        return parsed

    # -- login ---------------------------------------------------------------

    async def login(self, username: str, password: str, db: AsyncSession | None = None) -> dict:
        result = await self.post("login", {"username": username, "password": password}, authed=False, db=db)
        token = (result.get("data") or {}).get("access_token")
        if not token:
            raise HTTPException(status_code=502, detail=f"Login succeeded but no access_token in response: {result}")
        self.set_token(token)
        return result
