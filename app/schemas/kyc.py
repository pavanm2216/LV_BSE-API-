from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class _S(BaseModel):
    model_config = ConfigDict(extra="ignore")


class KYCLinkItem(_S):
    event: str
    member_code: str
    investor: Optional[dict] = None


class KYCLinkRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "items": [{
            "event": "kyc_link",
            "member_code": "92374",
            "investor": {"client_code": "DematUCCTest1"},
        }]
    }})
    items: List[KYCLinkItem]
