from __future__ import annotations

from typing import List, Literal, Optional

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


class OrderLine(BaseModelPermissive):
    """One order within an order_new / order_update call.

    type: "p" purchase, "r" redeem, "s" switch.
    """
    type: Literal["p", "r", "s"]
    mem_ord_ref_id: str
    investor: Investor
    member: Optional[str] = None
    mem_details: Optional[MemberDetails] = None
    scheme: str
    dest_scheme: Optional[str] = None
    amount: Optional[float] = None
    cur: Optional[str] = "INR"
    is_units: Optional[bool] = False
    all_units: Optional[bool] = False
    min_redeem_flag: Optional[bool] = False
    folio: Optional[str] = ""
    dest_folio: Optional[str] = None
    is_fresh: Optional[bool] = None
    phys_or_demat: Optional[str] = None  # "p" | "d"
    holder: List[Holder]
    is_nomination_opted: Optional[bool] = None
    nomination_auth_mode: Optional[str] = None
    nominee_soa: Optional[bool] = None
    nomination: Optional[List[Nomination]] = None
    payment_ref_id: Optional[str] = ""
    email: Optional[str] = None
    mobnum: Optional[str] = None
    exch_mandate_id: Optional[int] = None
    kyc_passed: Optional[bool] = None
    depository_acct: Optional[DepositoryAccount] = None
    bank_acct: Optional[BankAccount] = None
    dpc: Optional[bool] = None


class OrderNewRequest(BaseModelPermissive):
    orders: List[OrderLine]


class OrderUpdateRequest(OrderLine):
    id: int
    bank_ref_id: Optional[str] = None
    parent_client_code: Optional[str] = None


class OrderListRequest(Pagination):
    pass


class OrderGetRequest(BaseModelPermissive):
    id: int
    filter_param: Optional[dict] = None


class OrderCancelRequest(BaseModelPermissive):
    id: int
    investor: Investor
    remark: Optional[str] = None
