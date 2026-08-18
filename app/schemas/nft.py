from __future__ import annotations

from typing import List, Literal, Optional

from app.schemas.common import BaseModelPermissive


class NFTBaseRequest(BaseModelPermissive):
    """Common envelope for all NFT requests."""
    user_id: str
    member_code: str
    password: str
    amc: str
    rta: Literal["kfin", "cams"]
    member_id: str
    client_code: str
    entity_type: Optional[str] = None
    ref_id: Optional[str] = None


class NFTBankAccountChangeRequest(NFTBaseRequest):
    bank_change_info: List[BaseModelPermissive]


class NFTNomineeChangeRequest(NFTBaseRequest):
    nominee_change_info: List[BaseModelPermissive]


class NFTContactChangeRequest(NFTBaseRequest):
    contact_info: List[BaseModelPermissive]
