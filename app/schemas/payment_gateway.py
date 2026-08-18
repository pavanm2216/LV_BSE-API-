from __future__ import annotations

from typing import List, Literal, Optional

from app.schemas.common import BaseModelPermissive, Investor, MemberDetails


class PaymentGatewayServiceRequest(BaseModelPermissive):
    mem_details: Optional[MemberDetails] = None
    investor: Optional[Investor] = None
    order_ids: List[str]
    requested_method: Literal["exch_pg_page", "payment_info_data"]
    payment_mode: Optional[List[str]] = None  # "upi", "netbanking", "mandate"
    redirection_url: Optional[str] = None


class PaymentBankAccount(BaseModelPermissive):
    vpa: Optional[str] = None
    bank_id: Optional[str] = None
    account_number: Optional[str] = None
    ifsc: Optional[str] = None
    is_retail: Optional[bool] = None
    is_corporate: Optional[bool] = None


class PaymentDetails(BaseModelPermissive):
    bank_account: Optional[PaymentBankAccount] = None
    exch_mandate_id: Optional[str] = None


class SendPaymentInfoRequest(BaseModelPermissive):
    payment_mode: str
    order_ids: List[str]
    ucc: str
    member: Optional[str] = None
    amount: float
    currency: Optional[str] = "INR"
    redirection_url: Optional[str] = None
    payment_details: Optional[PaymentDetails] = None


class PaymentGatewayStatusRequest(BaseModelPermissive):
    order_id: Optional[str] = None
    payment_ref_id: Optional[str] = None
    include_audit: Optional[bool] = None
