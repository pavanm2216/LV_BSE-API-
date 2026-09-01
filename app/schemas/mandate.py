from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.common import BaseModelPermissive, Investor, MemberDetails, Pagination


class _S(BaseModel):
    model_config = ConfigDict(extra="ignore")


# ---------------------------------------------------------------------------
# Mandate Register
# ---------------------------------------------------------------------------

class MandateBankAccount(_S):
    ifsc: Optional[str] = None
    no: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None


class MandateRegisterRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "member": "92374",
        "investor": {"client_code": "DematUCCTest1"},
        "mandate_type": "ENACH",
        "amount": 5000,
        "investor_bank_details": {"ifsc": "HDFC0002729", "no": "50100178851121", "type": "SB"},
    }})
    member: Optional[str] = None
    investor: Optional[Investor] = None
    mem_details: Optional[MemberDetails] = None
    mandate_type: Optional[str] = None
    amount: Optional[float] = None
    investor_bank_details: Optional[MandateBankAccount] = None


# ---------------------------------------------------------------------------
# Mandate Cancel
# ---------------------------------------------------------------------------

class MandateCancelRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "ids": ["500043242"],
        "investor": {"client_code": "DematUCCTest1"},
    }})
    ids: List[str]
    investor: Optional[Investor] = None


# ---------------------------------------------------------------------------
# Mandate Get
# ---------------------------------------------------------------------------

class MandateGetRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "exch_mandate_id": "500043242",
    }})
    exch_mandate_id: str


# ---------------------------------------------------------------------------
# Mandate List
# ---------------------------------------------------------------------------

class MandateListFilterParam(_S):
    ucc: Optional[List[str]] = None
    status: Optional[List[str]] = None
    mandate_type: Optional[List[str]] = None


class MandateListRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "fields": ["ALL"],
        "start": 0,
        "length": 50,
        "filter_param": {},
    }})
    fields: Optional[List[str]] = None
    count_only: Optional[bool] = None
    start: Optional[int] = 0
    length: Optional[int] = 50
    filter_param: Optional[MandateListFilterParam] = None


# ---------------------------------------------------------------------------
# Mandate Update
# ---------------------------------------------------------------------------

class MandateIdentifier(_S):
    identifier_type: str
    file_name: Optional[str] = None
    file_blob: Optional[str] = None


class MandateUpdateRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "exch_mandate_id": "500043242",
        "investor": {"client_code": "DematUCCTest1"},
        "member": "92374",
    }})
    investor: Optional[Investor] = None
    exch_mandate_id: str
    member: Optional[str] = None
    identifier: Optional[MandateIdentifier] = None


# ---------------------------------------------------------------------------
# Mandate Link / Delink
# ---------------------------------------------------------------------------

class MandateLinkRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "reg_no": "202600000087970",
        "exch_mandate_id": "500043242",
    }})
    reg_no: str
    exch_mandate_id: str


class MandateDelinkRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "reg_nos": ["202600000087970"],
    }})
    reg_nos: List[str]
