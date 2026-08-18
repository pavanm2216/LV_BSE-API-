from __future__ import annotations

from typing import List

from app.schemas.common import BaseModelPermissive


class TwoFALinkItem(BaseModelPermissive):
    """One event item for v2/get_2fa_link.

    event selects the 2FA flow:
      'ucc_nom', 'ucc_elog', 'verify_mandate_cancel',
      'verify_sxp_reg', 'verify_order_cancel', 'verify_order_new', 'verify_order_update'.
    All other context fields (investor, order, member_code, etc.) pass through via extra='allow'.
    """
    event: str


class TwoFALinkRequest(BaseModelPermissive):
    items: List[TwoFALinkItem]
