"""
UCC endpoints.

add_ucc()/update_ucc() have ~15 real-world variants (resident/non-resident,
individual/non-individual, physical/demat/both, minor, joint, FPI/QFI...)
driven by which optional fields are present. Rather than one strict model per
variant (which would fight BSE's own conditional validation), AddUCCRequest /
UpdateUCCRequest type the fields common to every variant and allow the rest
through — see the sample payloads in the original Postman collection
(UCC folder) for the field combination needed for your specific case.
"""
from __future__ import annotations

from typing import List, Optional

from app.schemas.common import BaseModelPermissive, Investor, Holder, Pagination


class AddUCCRequest(BaseModelPermissive):
    investor: Investor
    is_multi_ucc: Optional[bool] = None
    parent_client_code: Optional[str] = None
    holding_nature: Optional[str] = None  # "SI" | "JO"
    tax_code: Optional[str] = None
    is_client_physical: Optional[bool] = None
    is_client_demat: Optional[bool] = None
    is_nomination_opted: Optional[bool] = None
    comm_mode: Optional[str] = None
    holder: Optional[List[dict]] = None  # holder blocks vary a lot by variant


class UpdateUCCRequest(BaseModelPermissive):
    investor: Investor
    member: Optional[dict] = None
    # every other field (bank_acct, nominee, fatca, address, dp_details, ...)
    # is accepted via the permissive base model — populate whichever block
    # corresponds to the update_ucc() sub-type you're calling.


class DeactivateUCCRequest(BaseModelPermissive):
    investor: Investor


class GetUCCRequest(BaseModelPermissive):
    member: Optional[dict] = None
    investor: Investor


class ListUCCRequest(Pagination):
    member: Optional[dict] = None
    investor: Optional[dict] = None
    ucc_status: Optional[str] = None
