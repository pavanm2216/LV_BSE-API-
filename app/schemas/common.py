"""Common building-block models shared by UCC / Orders / SXP payloads."""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class BaseModelPermissive(BaseModel):
    """Base class that allows extra fields to pass through untouched."""
    model_config = ConfigDict(extra="allow")


class Investor(BaseModel):
    model_config = ConfigDict(extra="ignore")
    ucc: Optional[str] = None
    client_code: Optional[str] = None


class MemberDetails(BaseModelPermissive):
    euin: Optional[str] = None
    euin_flag: Optional[bool] = None
    sub_br_code: Optional[str] = None
    sub_br_arn: Optional[str] = None
    partner_id: Optional[str] = None


class Holder(BaseModelPermissive):
    holder_rank: str
    email: Optional[str] = None
    mobnum: Optional[str] = None


class BankAccount(BaseModelPermissive):
    ifsc: Optional[str] = None
    no: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None


class DepositoryAccount(BaseModelPermissive):
    depository: Optional[str] = None
    dp_id: Optional[str] = None
    client_id: Optional[str] = None


class Identifier(BaseModelPermissive):
    identifier_type: str
    identifier_number: str
    expiry_date: Optional[str] = None


class Guardian(BaseModelPermissive):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[str] = None
    identifier: Optional[List[Identifier]] = None
    is_pan_exempt: Optional[bool] = None


class Nomination(BaseModelPermissive):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[str] = None
    nomination_percent: Optional[float] = None
    nomination_relation: Optional[str] = None
    is_pan_exempt: Optional[bool] = None
    pan_exempt_category: Optional[str] = None
    is_minor: Optional[bool] = None
    identifier: Optional[List[Identifier]] = None
    guardian: Optional[Guardian] = None


class Pagination(BaseModelPermissive):
    """Common list-endpoint pagination/filter envelope."""
    fields: Optional[List[str]] = None
    count_only: Optional[bool] = None
    start: Optional[int] = 0
    length: Optional[int] = 50
    filter_param: Optional[dict] = None
