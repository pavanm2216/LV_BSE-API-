from __future__ import annotations

from typing import List, Optional

from app.schemas.common import BaseModelPermissive, Pagination


class PaymentDetailGetRequest(BaseModelPermissive):
    order_id: Optional[str] = None
    bank_txn_ref: Optional[str] = None
    payment_ref_id: Optional[str] = None


class PaymentDetailListRequest(Pagination):
    bank_txn_ref: Optional[List[str]] = None
    payment_ref_id: Optional[List[str]] = None
