from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.common import (
    BankAccount,
    BaseModelPermissive,
    DepositoryAccount,
    Holder,
    Investor,
    MemberDetails,
    Nomination,
    Pagination,
)


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="ignore")


# ---------------------------------------------------------------------------
# order_new — Purchase Physical
# ---------------------------------------------------------------------------

class OrderNewPurchasePhysicalRequest(_StrictModel):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "orders": [{
            "type": "p",
            "mem_ord_ref_id": "2025290818714",
            "investor": {"client_code": "PhysicalUCCTest1"},
            "member": "92374",
            "scheme": "IDFCNF-GR",
            "amount": 1000,
            "cur": "INR",
            "is_units": False,
            "all_units": False,
            "min_redeem_flag": False,
            "folio": "",
            "is_fresh": True,
            "phys_or_demat": "p",
            "holder": [{"holder_rank": "1", "email": "", "mobnum": "9403231688"}],
            "is_nomination_opted": False,
            "nomination_auth_mode": "",
            "payment_ref_id": "",
            "email": "investor@example.com",
            "mobnum": "+919403231688",
            "kyc_passed": True,
            "dpc": True,
        }]
    }})
    orders: List[_PurchasePhysicalLine]


class _PurchasePhysicalLine(_StrictModel):
    type: str = "p"
    mem_ord_ref_id: str
    investor: Investor
    member: Optional[str] = None
    mem_details: Optional[MemberDetails] = None
    scheme: str
    amount: Optional[float] = None
    cur: Optional[str] = "INR"
    is_units: Optional[bool] = False
    all_units: Optional[bool] = False
    min_redeem_flag: Optional[bool] = False
    folio: Optional[str] = ""
    is_fresh: Optional[bool] = None
    phys_or_demat: Optional[str] = "p"
    holder: List[Holder]
    is_nomination_opted: Optional[bool] = None
    nomination_auth_mode: Optional[str] = None
    nominee_soa: Optional[bool] = None
    payment_ref_id: Optional[str] = ""
    email: Optional[str] = None
    mobnum: Optional[str] = None
    kyc_passed: Optional[bool] = None
    dpc: Optional[bool] = None


# Rebuild after forward ref
OrderNewPurchasePhysicalRequest.model_rebuild()


# ---------------------------------------------------------------------------
# order_new — Purchase with PAN Holder
# ---------------------------------------------------------------------------

class _PanIdentifier(_StrictModel):
    identifier_type: str = "pan"
    identifier_number: str


class _HolderWithPan(_StrictModel):
    holder_rank: str
    email: Optional[str] = None
    mobnum: Optional[str] = None
    identifier: Optional[List[_PanIdentifier]] = None


class _PurchasePanHolderLine(_StrictModel):
    type: str = "p"
    mem_ord_ref_id: str
    investor: Investor
    member: Optional[str] = None
    scheme: str
    amount: Optional[float] = None
    cur: Optional[str] = "INR"
    is_units: Optional[bool] = False
    all_units: Optional[bool] = False
    min_redeem_flag: Optional[bool] = False
    folio: Optional[str] = ""
    is_fresh: Optional[bool] = None
    phys_or_demat: Optional[str] = "p"
    holder: List[_HolderWithPan]
    is_nomination_opted: Optional[bool] = None
    nomination_auth_mode: Optional[str] = None
    payment_ref_id: Optional[str] = ""
    email: Optional[str] = None
    mobnum: Optional[str] = None
    kyc_passed: Optional[bool] = None
    dpc: Optional[bool] = None


class OrderNewPurchasePanHolderRequest(_StrictModel):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "orders": [{
            "type": "p",
            "mem_ord_ref_id": "2025290818715",
            "investor": {"client_code": "PhysicalUCCTest1"},
            "member": "92374",
            "scheme": "IDFCNF-GR",
            "amount": 1000,
            "cur": "INR",
            "is_units": False,
            "all_units": False,
            "folio": "",
            "is_fresh": True,
            "phys_or_demat": "p",
            "holder": [{"holder_rank": "1", "email": "", "mobnum": "9403231688",
                        "identifier": [{"identifier_type": "pan", "identifier_number": "FOCPM8532K"}]}],
            "is_nomination_opted": False,
            "payment_ref_id": "",
            "email": "investor@example.com",
            "mobnum": "+919403231688",
            "kyc_passed": True,
            "dpc": True,
        }]
    }})
    orders: List[_PurchasePanHolderLine]


# ---------------------------------------------------------------------------
# order_new — Purchase Demat
# ---------------------------------------------------------------------------

class _PurchaseDematLine(_StrictModel):
    type: str = "p"
    mem_ord_ref_id: str
    investor: Investor
    member: Optional[str] = None
    scheme: str
    amount: Optional[float] = None
    cur: Optional[str] = "INR"
    is_units: Optional[bool] = False
    all_units: Optional[bool] = False
    min_redeem_flag: Optional[bool] = False
    folio: Optional[str] = ""
    is_fresh: Optional[bool] = None
    phys_or_demat: Optional[str] = "d"
    holder: List[Holder]
    depository_acct: Optional[DepositoryAccount] = None
    is_nomination_opted: Optional[bool] = None
    nomination_auth_mode: Optional[str] = None
    payment_ref_id: Optional[str] = ""
    email: Optional[str] = None
    mobnum: Optional[str] = None
    kyc_passed: Optional[bool] = None
    dpc: Optional[bool] = None


class OrderNewPurchaseDematRequest(_StrictModel):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "orders": [{
            "type": "p",
            "mem_ord_ref_id": "2025290818716",
            "investor": {"client_code": "DematUCCTest1"},
            "member": "92374",
            "scheme": "IDFCNF-GR",
            "amount": 1000,
            "cur": "INR",
            "is_units": False,
            "all_units": False,
            "folio": "",
            "is_fresh": True,
            "phys_or_demat": "d",
            "holder": [{"holder_rank": "1", "email": "", "mobnum": "9403231688"}],
            "depository_acct": {"depository": "CDSL", "dp_id": "12345678", "client_id": "12345678"},
            "is_nomination_opted": False,
            "payment_ref_id": "",
            "email": "parth.ashtikar@bseindia.com",
            "mobnum": "+919403231688",
            "kyc_passed": True,
            "dpc": True,
        }]
    }})
    orders: List[_PurchaseDematLine]


# ---------------------------------------------------------------------------
# order_new — Purchase with Nomination
# ---------------------------------------------------------------------------

class _PurchaseNominationLine(_StrictModel):
    type: str = "p"
    mem_ord_ref_id: str
    investor: Investor
    member: Optional[str] = None
    scheme: str
    amount: Optional[float] = None
    cur: Optional[str] = "INR"
    is_units: Optional[bool] = False
    all_units: Optional[bool] = False
    min_redeem_flag: Optional[bool] = False
    folio: Optional[str] = ""
    is_fresh: Optional[bool] = None
    phys_or_demat: Optional[str] = "p"
    holder: List[Holder]
    is_nomination_opted: Optional[bool] = True
    nomination_auth_mode: Optional[str] = None
    nominee_soa: Optional[bool] = None
    nomination: Optional[List[Nomination]] = None
    payment_ref_id: Optional[str] = ""
    email: Optional[str] = None
    mobnum: Optional[str] = None
    kyc_passed: Optional[bool] = None
    dpc: Optional[bool] = None


class OrderNewPurchaseNominationRequest(_StrictModel):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "orders": [{
            "type": "p",
            "mem_ord_ref_id": "2025290818717",
            "investor": {"client_code": "PhysicalUCCTest1"},
            "member": "92374",
            "scheme": "IDFCNF-GR",
            "amount": 1000,
            "cur": "INR",
            "is_units": False,
            "all_units": False,
            "folio": "",
            "is_fresh": True,
            "phys_or_demat": "p",
            "holder": [{"holder_rank": "1", "email": "", "mobnum": "9403231688"}],
            "is_nomination_opted": True,
            "nomination_auth_mode": "O",
            "nomination": [{"first_name": "Jane", "last_name": "Doe",
                            "nomination_percent": 100.0, "nomination_relation": "SPOUSE",
                            "is_pan_exempt": False}],
            "payment_ref_id": "",
            "email": "investor@example.com",
            "mobnum": "+919403231688",
            "kyc_passed": True,
            "dpc": True,
        }]
    }})
    orders: List[_PurchaseNominationLine]


# ---------------------------------------------------------------------------
# order_new — Redeem Physical
# ---------------------------------------------------------------------------

class _RedeemPhysicalLine(_StrictModel):
    type: str = "r"
    mem_ord_ref_id: str
    investor: Investor
    member: Optional[str] = None
    scheme: str
    amount: Optional[float] = None
    cur: Optional[str] = "INR"
    is_units: Optional[bool] = False
    all_units: Optional[bool] = False
    min_redeem_flag: Optional[bool] = False
    folio: Optional[str] = ""
    phys_or_demat: Optional[str] = "p"
    holder: List[Holder]
    payment_ref_id: Optional[str] = ""
    email: Optional[str] = None
    mobnum: Optional[str] = None
    bank_acct: Optional[BankAccount] = None
    kyc_passed: Optional[bool] = None
    dpc: Optional[bool] = None


class OrderNewRedeemPhysicalRequest(_StrictModel):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "orders": [{
            "type": "r",
            "mem_ord_ref_id": "2025290818718",
            "investor": {"client_code": "PhysicalUCCTest1"},
            "member": "92374",
            "scheme": "IDFCNF-GR",
            "amount": 500,
            "cur": "INR",
            "is_units": False,
            "all_units": False,
            "min_redeem_flag": False,
            "folio": "12345678",
            "phys_or_demat": "p",
            "holder": [{"holder_rank": "1", "email": "", "mobnum": "9403231688"}],
            "payment_ref_id": "",
            "email": "investor@example.com",
            "mobnum": "+919403231688",
            "kyc_passed": True,
            "dpc": True,
        }]
    }})
    orders: List[_RedeemPhysicalLine]


# ---------------------------------------------------------------------------
# order_new — Redeem Demat
# ---------------------------------------------------------------------------

class _RedeemDematLine(_StrictModel):
    type: str = "r"
    mem_ord_ref_id: str
    investor: Investor
    member: Optional[str] = None
    scheme: str
    amount: Optional[float] = None
    cur: Optional[str] = "INR"
    is_units: Optional[bool] = False
    all_units: Optional[bool] = False
    min_redeem_flag: Optional[bool] = False
    folio: Optional[str] = ""
    phys_or_demat: Optional[str] = "d"
    holder: List[Holder]
    depository_acct: Optional[DepositoryAccount] = None
    payment_ref_id: Optional[str] = ""
    email: Optional[str] = None
    mobnum: Optional[str] = None
    kyc_passed: Optional[bool] = None
    dpc: Optional[bool] = None


class OrderNewRedeemDematRequest(_StrictModel):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "orders": [{
            "type": "r",
            "mem_ord_ref_id": "2025290818719",
            "investor": {"client_code": "DematUCCTest1"},
            "member": "92374",
            "scheme": "IDFCNF-GR",
            "amount": 500,
            "cur": "INR",
            "is_units": False,
            "all_units": False,
            "folio": "12345678",
            "phys_or_demat": "d",
            "holder": [{"holder_rank": "1", "email": "", "mobnum": "9403231688"}],
            "depository_acct": {"depository": "CDSL", "dp_id": "12345678", "client_id": "12345678"},
            "payment_ref_id": "",
            "email": "parth.ashtikar@bseindia.com",
            "mobnum": "+919403231688",
            "kyc_passed": True,
            "dpc": True,
        }]
    }})
    orders: List[_RedeemDematLine]


# ---------------------------------------------------------------------------
# order_new — Switch Physical
# ---------------------------------------------------------------------------

class _SwitchPhysicalLine(_StrictModel):
    type: str = "s"
    mem_ord_ref_id: str
    investor: Investor
    member: Optional[str] = None
    scheme: str
    dest_scheme: str
    amount: Optional[float] = None
    cur: Optional[str] = "INR"
    is_units: Optional[bool] = False
    all_units: Optional[bool] = False
    folio: Optional[str] = ""
    dest_folio: Optional[str] = ""
    phys_or_demat: Optional[str] = "p"
    holder: List[Holder]
    payment_ref_id: Optional[str] = ""
    email: Optional[str] = None
    mobnum: Optional[str] = None
    kyc_passed: Optional[bool] = None
    dpc: Optional[bool] = None


class OrderNewSwitchPhysicalRequest(_StrictModel):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "orders": [{
            "type": "s",
            "mem_ord_ref_id": "2025290818720",
            "investor": {"client_code": "PhysicalUCCTest1"},
            "member": "92374",
            "scheme": "IDFCNF-GR",
            "dest_scheme": "IDFCNF-DP",
            "amount": 1000,
            "cur": "INR",
            "is_units": False,
            "all_units": False,
            "folio": "12345678",
            "dest_folio": "",
            "phys_or_demat": "p",
            "holder": [{"holder_rank": "1", "email": "", "mobnum": "9403231688"}],
            "payment_ref_id": "",
            "email": "investor@example.com",
            "mobnum": "+919403231688",
            "kyc_passed": True,
            "dpc": True,
        }]
    }})
    orders: List[_SwitchPhysicalLine]


# ---------------------------------------------------------------------------
# order_new — Switch Demat
# ---------------------------------------------------------------------------

class _SwitchDematLine(_StrictModel):
    type: str = "s"
    mem_ord_ref_id: str
    investor: Investor
    member: Optional[str] = None
    scheme: str
    dest_scheme: str
    amount: Optional[float] = None
    cur: Optional[str] = "INR"
    is_units: Optional[bool] = False
    all_units: Optional[bool] = False
    folio: Optional[str] = ""
    dest_folio: Optional[str] = ""
    phys_or_demat: Optional[str] = "d"
    holder: List[Holder]
    depository_acct: Optional[DepositoryAccount] = None
    payment_ref_id: Optional[str] = ""
    email: Optional[str] = None
    mobnum: Optional[str] = None
    kyc_passed: Optional[bool] = None
    dpc: Optional[bool] = None


class OrderNewSwitchDematRequest(_StrictModel):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "orders": [{
            "type": "s",
            "mem_ord_ref_id": "2025290818721",
            "investor": {"client_code": "DematUCCTest1"},
            "member": "92374",
            "scheme": "IDFCNF-GR",
            "dest_scheme": "IDFCNF-DP",
            "amount": 1000,
            "cur": "INR",
            "is_units": False,
            "all_units": False,
            "folio": "12345678",
            "dest_folio": "",
            "phys_or_demat": "d",
            "holder": [{"holder_rank": "1", "email": "", "mobnum": "9403231688"}],
            "depository_acct": {"depository": "CDSL", "dp_id": "12345678", "client_id": "12345678"},
            "payment_ref_id": "",
            "email": "parth.ashtikar@bseindia.com",
            "mobnum": "+919403231688",
            "kyc_passed": True,
            "dpc": True,
        }]
    }})
    orders: List[_SwitchDematLine]


# ---------------------------------------------------------------------------
# order_update_purchase
# ---------------------------------------------------------------------------

class OrderUpdateRequest(_StrictModel):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "id": 123456,
        "type": "p",
        "mem_ord_ref_id": "2025290818714",
        "investor": {"client_code": "PhysicalUCCTest1"},
        "member": "92374",
        "scheme": "IDFCNF-GR",
        "amount": 1000,
        "cur": "INR",
        "is_units": False,
        "all_units": False,
        "folio": "",
        "phys_or_demat": "p",
        "holder": [{"holder_rank": "1", "email": "", "mobnum": "9403231688"}],
        "bank_ref_id": "BANK123456",
        "payment_ref_id": "",
        "email": "investor@example.com",
        "mobnum": "+919403231688",
        "kyc_passed": True,
        "dpc": True,
    }})
    id: int
    type: str
    mem_ord_ref_id: str
    investor: Investor
    member: Optional[str] = None
    scheme: str
    amount: Optional[float] = None
    cur: Optional[str] = "INR"
    is_units: Optional[bool] = False
    all_units: Optional[bool] = False
    min_redeem_flag: Optional[bool] = False
    folio: Optional[str] = ""
    dest_folio: Optional[str] = None
    dest_scheme: Optional[str] = None
    phys_or_demat: Optional[str] = None
    holder: List[Holder]
    bank_ref_id: Optional[str] = None
    payment_ref_id: Optional[str] = ""
    email: Optional[str] = None
    mobnum: Optional[str] = None
    kyc_passed: Optional[bool] = None
    dpc: Optional[bool] = None
    parent_client_code: Optional[str] = None


# ---------------------------------------------------------------------------
# order_list / order_get / order_cancel
# ---------------------------------------------------------------------------

class OrderListRequest(Pagination):
    pass


class OrderGetRequest(_StrictModel):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "id": 123456
    }})
    id: int
    filter_param: Optional[dict] = None


class OrderCancelRequest(_StrictModel):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "id": 123456,
        "investor": {"client_code": "PhysicalUCCTest1"},
        "remark": "Cancelled by investor",
    }})
    id: int
    investor: Investor
    remark: Optional[str] = None


# Keep generic for backward compat
class OrderNewRequest(_StrictModel):
    orders: List[dict]
