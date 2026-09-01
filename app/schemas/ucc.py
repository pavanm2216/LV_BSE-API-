"""
UCC schemas aligned with BSE STARMF 2.0 add_ucc payload.
"""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

UccStatus = Literal[
    "ACTIVE", "INACTIVE", "HOLD",
    "PENDING_AUTHENTICATION", "PENDING_APPROVAL", "REJECTED",
]

from pydantic import BaseModel, ConfigDict

from app.schemas.common import BaseModelPermissive, Investor, Pagination


class _StrictModel(BaseModel):
    """Base for top-level request models — no extra fields in Swagger."""
    model_config = ConfigDict(extra="ignore")


# ---------------------------------------------------------------------------
# Shared sub-objects
# ---------------------------------------------------------------------------

class PersonName(BaseModel):
    model_config = ConfigDict(extra="ignore")
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None


class Contact(BaseModel):
    model_config = ConfigDict(extra="ignore")
    contact_number: Optional[str] = None
    country_code: Optional[str] = None
    whose_contact_number: Optional[str] = None
    email_address: Optional[str] = None
    whose_email_address: Optional[str] = None
    contact_type: Optional[str] = None


class Address(BaseModel):
    model_config = ConfigDict(extra="ignore")
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    address_line_3: Optional[str] = None
    comm_mode: Optional[str] = None
    postalcode: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    City: Optional[str] = None          # BSE uses capital-C
    address_id: Optional[int] = None


class IdentifierItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    identifier_type: str
    identifier_number: Optional[str] = None
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    identifier_size: Optional[int] = None
    extension: Optional[str] = None
    blob_id: Optional[str] = None
    file_blob: Optional[str] = None
    additional_info: Optional[Any] = None


class Guardian(BaseModel):
    model_config = ConfigDict(extra="ignore")
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[str] = None
    is_pan_exempt: Optional[bool] = None
    pan_exempt_category: Optional[str] = None
    identifier: Optional[List[IdentifierItem]] = None


class Nomination(BaseModel):
    model_config = ConfigDict(extra="ignore")
    person: Optional[PersonName] = None
    contact: Optional[Contact] = None
    comm_addr: Optional[Address] = None
    nomination_percent: Optional[str] = None
    nomination_relation: Optional[str] = None
    is_pan_exempt: Optional[bool] = None
    pan_exempt_category: Optional[str] = None
    is_minor: Optional[bool] = None
    identifier: Optional[List[IdentifierItem]] = None
    guardian: Optional[Guardian] = None


class Holder(BaseModel):
    model_config = ConfigDict(extra="ignore")
    holder_rank: str
    occ_code: Optional[str] = None
    auth_mode: Optional[str] = None
    is_pan_exempt: Optional[bool] = None
    pan_exempt_category: Optional[str] = None
    identifier: Optional[List[IdentifierItem]] = None
    kyc_type: Optional[str] = None
    ckyc_number: Optional[str] = None
    person: Optional[PersonName] = None
    contact: Optional[List[Contact]] = None
    nomination: Optional[List[Nomination]] = None


class BankAccount(BaseModel):
    model_config = ConfigDict(extra="ignore")
    ifsc_code: Optional[str] = None
    bank_acc_num: Optional[str] = None
    bank_acc_type: Optional[str] = None
    account_owner: Optional[str] = None


class DepositoryIdentifier(BaseModel):
    model_config = ConfigDict(extra="ignore")
    add: Optional[List[IdentifierItem]] = None
    delete: Optional[List[IdentifierItem]] = None


class Depository(BaseModel):
    model_config = ConfigDict(extra="ignore")
    depository_type: Optional[str] = None   # used in add_ucc
    depository_code: Optional[str] = None   # NSDL / CDSL
    dp_id: Optional[str] = None
    client_id: Optional[str] = None
    cmbp_id: Optional[str] = None
    bank_account: Optional[str] = None      # bank acc num linked to demat
    account_owner: Optional[str] = None
    identifier: Optional[DepositoryIdentifier] = None


class TaxResidency(BaseModel):
    model_config = ConfigDict(extra="ignore")
    country: Optional[str] = None
    tax_id_no: Optional[str] = None
    tax_id_type: Optional[str] = None


class Fatca(BaseModel):
    model_config = ConfigDict(extra="ignore")
    HolderRank: Optional[str] = None
    place_of_birth: Optional[str] = None
    country_of_birth: Optional[str] = None
    client_name: Optional[str] = None
    investor_type: Optional[str] = None
    dob: Optional[str] = None
    father_name: Optional[str] = None
    spouse_name: Optional[str] = None
    address_type: Optional[str] = None
    occ_code: Optional[str] = None
    occ_type: Optional[str] = None
    tax_status: Optional[str] = None
    exemption_code: Optional[str] = None
    identifier: Optional[IdentifierItem] = None
    corporate_service_sector: Optional[str] = None
    wealth_source: Optional[str] = None
    income_slab: Optional[str] = None
    net_worth: Optional[float] = None
    date_of_net_worth: Optional[str] = None
    politically_exposed: Optional[str] = None
    is_self_declared: Optional[bool] = None
    data_source: Optional[str] = None
    tax_residency: Optional[List[TaxResidency]] = None


class MemberRef(BaseModel):
    model_config = ConfigDict(extra="ignore")
    member_id: Optional[str] = None


class NominationApproval(BaseModel):
    model_config = ConfigDict(extra="ignore")


# ---------------------------------------------------------------------------
# Top-level request models
# ---------------------------------------------------------------------------

class AddUCCRequest(_StrictModel):
    investor: Investor
    is_multi_ucc: Optional[bool] = None
    parent_client_code: Optional[str] = None
    pms_client: Optional[bool] = None
    pms_code: Optional[str] = None
    holding_nature: Optional[str] = None
    tax_status: Optional[str] = None
    tax_code: Optional[str] = None
    rdmp_idcw_pay_mode: Optional[str] = None
    is_client_physical: Optional[bool] = None
    is_client_demat: Optional[bool] = None
    is_nomination_opted: Optional[bool] = None
    nominee_soa: Optional[bool] = None
    nomination_auth_mode: Optional[str] = None
    nomination_approval: Optional[NominationApproval] = None
    comm_mode: Optional[str] = None
    onboarding: Optional[str] = None
    holder: Optional[List[Holder]] = None
    comm_addr: Optional[Address] = None
    foreign_addr: Optional[Address] = None
    depository: Optional[List[Depository]] = None
    bank_account: Optional[List[BankAccount]] = None
    fatca: Optional[List[Fatca]] = None
    aof: Optional[Dict[str, Any]] = None
    aof_ria: Optional[Dict[str, Any]] = None
    identifiers: Optional[List[IdentifierItem]] = None


# --- Update sub-models ---

class BankAccountUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    add: Optional[List[BankAccount]] = None
    delete: Optional[List[BankAccount]] = None


class DepositoryUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    add: Optional[List[Depository]] = None
    delete: Optional[List[Depository]] = None


class HolderUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    holder_rank: Optional[str] = None
    occ_code: Optional[str] = None
    auth_mode: Optional[str] = None
    is_pan_exempt: Optional[bool] = None
    pan_exempt_category: Optional[str] = None
    identifier: Optional[List[IdentifierItem]] = None
    kyc_type: Optional[str] = None
    ckyc_number: Optional[str] = None
    person: Optional[PersonName] = None
    contact: Optional[List[Contact]] = None
    nomination: Optional[List[Nomination]] = None
    add: Optional[List[dict]] = None


class FatcaUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    ubo: Optional[dict] = None
    npo: Optional[dict] = None


# ---------------------------------------------------------------------------
# Update UCC — one model per BSE sub-type
# ---------------------------------------------------------------------------

class UpdateUCCStatusRequest(_StrictModel):
    """Individual UCC status update."""
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "member": {"member_id": "92374"},
        "investor": {"client_code": "DematUCCTest1"},
        "ucc_status": "ACTIVE",
    }})
    member: Optional[MemberRef] = None
    investor: Investor
    parent_client_code: Optional[str] = None
    ucc_status: UccStatus


class UpdateUCCProfileRequest(_StrictModel):
    """Profile update — Holding Nature, Holder, FATCA."""
    member: Optional[MemberRef] = None
    investor: Investor
    parent_client_code: Optional[str] = None
    holder: Optional[HolderUpdate] = None
    fatca: Optional[List[Fatca]] = None
    holding_nature: Optional[str] = None


class UpdateUCCBankRequest(_StrictModel):
    """Bank account add/update/delete."""
    member: Optional[MemberRef] = None
    investor: Investor
    parent_client_code: Optional[str] = None
    bank_account: BankAccountUpdate


class UpdateUCCPersonRequest(_StrictModel):
    """Update person details for a holder."""
    member: Optional[MemberRef] = None
    investor: Investor
    parent_client_code: Optional[str] = None
    holder: List[HolderUpdate]


class UpdateUCCNomineeRequest(_StrictModel):
    """Update nomination — full replacement set."""
    member: Optional[MemberRef] = None
    investor: Investor
    parent_client_code: Optional[str] = None
    is_nomination_opted: Optional[bool] = None
    nomination_auth_mode: Optional[str] = None
    nominee_soa: Optional[bool] = None
    holder: List[HolderUpdate]


class UpdateUCCFatcaRequest(_StrictModel):
    """FATCA full replacement."""
    member: Optional[MemberRef] = None
    investor: Investor
    parent_client_code: Optional[str] = None
    holder: Optional[HolderUpdate] = None
    fatca: FatcaUpdate


class UpdateUCCCommAddrRequest(_StrictModel):
    """Communication address update."""
    member: Optional[MemberRef] = None
    investor: Investor
    parent_client_code: Optional[str] = None
    comm_addr: Address


class UpdateUCCForeignAddrRequest(_StrictModel):
    """Foreign address update."""
    member: Optional[MemberRef] = None
    investor: Investor
    parent_client_code: Optional[str] = None
    foreign_addr: Address


class UpdateUCCDepositoryRequest(_StrictModel):
    """Depository account add/update/delete."""
    member: Optional[MemberRef] = None
    investor: Investor
    parent_client_code: Optional[str] = None
    is_client_demat: Optional[bool] = None
    is_client_physical: Optional[bool] = None
    depository: DepositoryUpdate


class UpdateUCCContactRequest(_StrictModel):
    """Contact details update for a holder."""
    member: Optional[MemberRef] = None
    investor: Investor
    parent_client_code: Optional[str] = None
    holder: List[HolderUpdate]


class UpdateUCCIdentifierRequest(_StrictModel):
    """Identifier documents update."""
    member: Optional[MemberRef] = None
    investor: Investor
    parent_client_code: Optional[str] = None
    holder: Optional[List[HolderUpdate]] = None
    identifiers: Optional[List[IdentifierItem]] = None


class UpdateUCCHoldingNatureRequest(_StrictModel):
    """Holding nature change e.g. SI to JO."""
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "member": {"member_id": "92374"},
        "investor": {"client_code": "DematUCCTest1"},
        "holding_nature": "SI",
    }})
    member: Optional[MemberRef] = None
    investor: Investor
    parent_client_code: Optional[str] = None
    holding_nature: str
    holder: Optional[List[HolderUpdate]] = None


class UpdateUCCHolderObjectRequest(_StrictModel):
    """Update UCC Holder Object (add new holder)."""
    member: Optional[MemberRef] = None
    investor: Investor
    parent_client_code: Optional[str] = None
    holder: HolderUpdate


# Keep generic UpdateUCCRequest for backward compat
class UpdateUCCRequest(_StrictModel):
    member: Optional[MemberRef] = None
    investor: Investor
    parent_client_code: Optional[str] = None
    holder: Optional[HolderUpdate] = None
    bank_account: Optional[BankAccountUpdate] = None
    depository: Optional[DepositoryUpdate] = None
    comm_addr: Optional[Address] = None
    foreign_addr: Optional[Address] = None
    fatca: Optional[FatcaUpdate] = None
    nominee_soa: Optional[bool] = None
    identifiers: Optional[List[IdentifierItem]] = None
    ucc_status: Optional[UccStatus] = None
    holding_nature: Optional[str] = None


class DeactivateUCCRequest(_StrictModel):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "member": {"member_id": "92374"},
        "investor": {"client_code": "DematUCCTest1"},
        "ucc_status": "INACTIVE",
    }})
    investor: Investor
    member: Optional[MemberRef] = None
    ucc_status: UccStatus = "INACTIVE"


class GetUCCRequest(_StrictModel):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "member": {"member_id": "92374"},
        "investor": {"client_code": "DematUCCTest1"},
    }})
    member: Optional[MemberRef] = None
    investor: Investor


class ListUCCFilterParam(BaseModel):
    model_config = ConfigDict(extra="ignore")
    tax_status: Optional[str] = None
    holding_nature: Optional[str] = None
    is_client_physical: Optional[bool] = None
    is_client_demat: Optional[bool] = None
    parent_client_code: Optional[str] = None


class ListUCCRequest(_StrictModel):
    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "ucc_status": "ACTIVE",
                "count_only": False,
                "start": 0,
                "length": 50,
                "fields": ["ALL"],
            }
        },
    )
    member: Optional[MemberRef] = None
    investor: Optional[Investor] = None
    ucc_status: Optional[UccStatus] = None
    fields: Optional[List[str]] = None
    count_only: Optional[bool] = None
    start: Optional[int] = 0
    length: Optional[int] = 50
    filter_param: Optional[ListUCCFilterParam] = None
