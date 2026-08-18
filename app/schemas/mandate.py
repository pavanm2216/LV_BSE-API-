from __future__ import annotations

from typing import List, Optional

from app.schemas.common import BankAccount, BaseModelPermissive, Investor, MemberDetails, Pagination


class MandateRegisterRequest(BaseModelPermissive):
    """Permissive — BSE has 5 mandate variants (UPI Autopay Intent/Collect, ENACH, NACH).
    Common fields typed; mode-specific fields pass through via extra='allow'."""
    member: Optional[str] = None
    investor: Optional[Investor] = None
    mem_details: Optional[MemberDetails] = None
    investor_bank_details: Optional[BankAccount] = None


class MandateCancelRequest(BaseModelPermissive):
    ids: List[str]
    investor: Optional[Investor] = None


class MandateGetRequest(BaseModelPermissive):
    exch_mandate_id: str


class MandateListRequest(Pagination):
    pass


class MandateIdentifier(BaseModelPermissive):
    identifier_type: str
    file_name: Optional[str] = None
    file_blob: Optional[str] = None  # base64


class MandateUpdateRequest(BaseModelPermissive):
    investor: Optional[Investor] = None
    exch_mandate_id: str
    member: Optional[str] = None
    identifier: Optional[MandateIdentifier] = None


class MandateLinkRequest(BaseModelPermissive):
    reg_no: str
    exch_mandate_id: str


class MandateDelinkRequest(BaseModelPermissive):
    reg_nos: List[str]
