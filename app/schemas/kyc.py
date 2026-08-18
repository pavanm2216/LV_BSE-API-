from __future__ import annotations

from typing import List

from app.schemas.common import BaseModelPermissive


class KYCLinkItem(BaseModelPermissive):
    """One item in the v2/get_kyc_link list body."""
    event: str
    member_code: str


class KYCLinkRequest(BaseModelPermissive):
    items: List[KYCLinkItem]
