from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.common import Investor, MemberDetails


class _S(BaseModel):
    model_config = ConfigDict(extra="ignore")


class PaymentGatewayServiceRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "investor": {"client_code": "DematUCCTest1"},
        "order_ids": ["5001436968"],
        "requested_method": "exch_pg_page",
        "payment_mode": ["upi"],
        "redirection_url": "https://your-app.com/payment/callback",
    }})
    mem_details: Optional[MemberDetails] = None
    investor: Optional[Investor] = None
    order_ids: List[str]
    requested_method: Literal["exch_pg_page", "payment_info_data"]
    payment_mode: Optional[List[str]] = None
    redirection_url: Optional[str] = None


class PaymentBankAccount(_S):
    vpa: Optional[str] = None
    bank_id: Optional[str] = None
    account_number: Optional[str] = None
    ifsc: Optional[str] = None
    is_retail: Optional[bool] = None
    is_corporate: Optional[bool] = None


class PaymentDetails(_S):
    bank_account: Optional[PaymentBankAccount] = None
    exch_mandate_id: Optional[str] = None


class SendPaymentInfoRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "payment_mode": "upi",
        "order_ids": ["5001436968"],
        "ucc": "DematUCCTest1",
        "member": "92374",
        "amount": 1000.0,
        "currency": "INR",
        "redirection_url": "https://your-app.com/payment/callback",
        "payment_details": {"bank_account": {"vpa": "investor@upi"}},
    }})
    payment_mode: str
    order_ids: List[str]
    ucc: str
    member: Optional[str] = None
    amount: float
    currency: Optional[str] = "INR"
    redirection_url: Optional[str] = None
    payment_details: Optional[PaymentDetails] = None


class PaymentGatewayStatusRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "order_id": "5001436968",
    }})
    order_id: Optional[str] = None
    payment_ref_id: Optional[str] = None
    include_audit: Optional[bool] = None
