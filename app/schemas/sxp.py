from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.common import Holder, Investor, MemberDetails


class _S(BaseModel):
    model_config = ConfigDict(extra="ignore")


class SXPRegisterRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "sxp_type": "sip",
        "mem_sxp_ref_id": "SIP-2026-001",
        "investor": {"client_code": "DematUCCTest1"},
        "member": "92374",
        "src_scheme": "007-DP",
        "amount": 1000,
        "cur": "INR",
        "is_fresh": True,
        "phys_or_demat": "d",
        "start_date": "2026-10-01",
        "end_date": "2027-09-01",
        "freq": "m",
        "txn_date": 1,
        "holder": [{"holder_rank": "1", "email": "", "mobnum": "9403231688"}],
        "kyc_passed": True,
        "dpc": True,
        "payment_ref_id": "",
    }})
    sxp_type: Literal["sip", "xsip", "swp", "stp"]
    mem_sxp_ref_id: Optional[str] = None
    investor: Investor
    member: Optional[str] = None
    mem_details: Optional[MemberDetails] = None
    src_scheme: str
    dest_scheme: Optional[str] = None
    kyc_passed: Optional[bool] = None
    amc_code: Optional[str] = None
    exch_mandate_id: Optional[int] = None
    amount: float
    cur: Optional[str] = "INR"
    is_fresh: Optional[bool] = None
    src_folio: Optional[str] = None
    dest_folio: Optional[str] = None
    phys_or_demat: Optional[str] = None
    isunits: Optional[bool] = False
    min_redeem_flag: Optional[bool] = None
    dpc: Optional[bool] = None
    start_date: str
    end_date: Optional[str] = None
    freq: str
    txn_date: int
    payment_ref_id: Optional[str] = ""
    holder: List[Holder]
    remark: Optional[str] = None
    email: Optional[str] = None
    mobnum: Optional[str] = None
    first_order_today: Optional[bool] = None


class SXPCancelRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "reg_no": "202600000087970",
        "sxp_type": "sip",
        "reason_cd": 1,
        "reason_cd_msg": "Investor request",
    }})
    reg_no: str
    reason_cd: int
    reason_cd_msg: Optional[str] = None
    sxp_type: str


class SXPPauseRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "reg_no": "202600000087970",
        "ninstallments": 2,
        "paused_from": "2026-10-01",
    }})
    reg_no: str
    ninstallments: int
    paused_from: str


class SXPResumeRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "reg_no": "202600000087970",
        "resume_reason": "Investor request",
    }})
    reg_no: str
    resume_reason: Optional[str] = None


class SXPGetRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "reg_no": "202600000087970",
        "sxp_type": "sip",
    }})
    reg_no: str
    sxp_type: str


class SXPTopupRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "reg_num": "202600000087970",
        "amount": 2000,
        "cur": "INR",
    }})
    reg_num: str
    mem_sxp_ref_id: Optional[str] = None
    amount: float
    cur: Optional[str] = "INR"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    freq: Optional[str] = None
    txn_date: Optional[int] = None
    payment_ref_id: Optional[str] = ""
    remark: Optional[str] = None
    first_order_today: Optional[bool] = None
    email: Optional[str] = None
    mobnum: Optional[str] = None


class SXPGetHistoryRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "reg_no": "202600000087970",
        "fields": ["ALL"],
    }})
    reg_no: str
    fields: Optional[List[str]] = None
    filter_param: Optional[dict] = None


class SXPListFilterParam(_S):
    sxp_type: Optional[List[str]] = None   # ["sip"] / ["xsip"] / ["swp"] / ["stp"]
    status: Optional[List[str]] = None
    ucc: Optional[List[str]] = None
    amc_code: Optional[str] = None
    placed_at_after: Optional[str] = None
    placed_at_before: Optional[str] = None


class SXPListRequest(_S):
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
    filter_param: Optional[SXPListFilterParam] = None
