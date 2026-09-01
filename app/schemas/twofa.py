from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class _S(BaseModel):
    model_config = ConfigDict(extra="ignore")


class TwoFALinkItem(_S):
    event: str
    investor: Optional[dict] = None
    member_code: Optional[str] = None
    order_id: Optional[str] = None
    reg_no: Optional[str] = None


class TwoFALinkRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "items": [{
            "event": "ucc_nom",
            "investor": {"client_code": "DematUCCTest1"},
            "member_code": "92374",
        }]
    }})
    items: List[TwoFALinkItem]
