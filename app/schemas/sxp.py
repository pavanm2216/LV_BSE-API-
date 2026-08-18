from __future__ import annotations

from typing import List, Literal, Optional

from app.schemas.common import BaseModelPermissive, Holder, Investor, MemberDetails, Pagination


class SXPRegisterRequest(BaseModelPermissive):
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
    freq: str  # "m" monthly, "y" yearly, etc.
    txn_date: int
    payment_ref_id: Optional[str] = ""
    holder: List[Holder]
    remark: Optional[str] = None
    email: Optional[str] = None
    mobnum: Optional[str] = None
    first_order_today: Optional[bool] = None


class SXPCancelRequest(BaseModelPermissive):
    reg_no: str
    reason_cd: int
    reason_cd_msg: Optional[str] = None
    sxp_type: str


class SXPPauseRequest(BaseModelPermissive):
    reg_no: str
    ninstallments: int
    paused_from: str


class SXPResumeRequest(BaseModelPermissive):
    reg_no: str
    resume_reason: Optional[str] = None


class SXPGetRequest(BaseModelPermissive):
    reg_no: str
    sxp_type: str


class SXPTopupRequest(BaseModelPermissive):
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


class SXPGetHistoryRequest(BaseModelPermissive):
    reg_no: str
    fields: Optional[List[str]] = None
    filter_param: Optional[dict] = None


class SXPListRequest(Pagination):
    pass
