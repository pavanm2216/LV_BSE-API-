from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class _S(BaseModel):
    model_config = ConfigDict(extra="ignore")


class PaymentDetailGetRequest(_S):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "payment_ref_id": "20260000008797020260901",
    }})
    order_id: Optional[str] = None
    bank_txn_ref: Optional[str] = None
    payment_ref_id: Optional[str] = None


class PaymentDetailListFilterParam(_S):
    ucc: Optional[List[str]] = None
    status: Optional[List[str]] = None
    placed_at_after: Optional[str] = None
    placed_at_before: Optional[str] = None


class PaymentDetailListRequest(_S):
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
    bank_txn_ref: Optional[List[str]] = None
    payment_ref_id: Optional[List[str]] = None
    filter_param: Optional[PaymentDetailListFilterParam] = None
