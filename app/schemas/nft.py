from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict


class _S(BaseModel):
    model_config = ConfigDict(extra="ignore")


class NFTBankChangeInfo(_S):
    old_ifsc: Optional[str] = None
    old_acc_no: Optional[str] = None
    new_ifsc: Optional[str] = None
    new_acc_no: Optional[str] = None
    new_acc_type: Optional[str] = None


class NFTNomineeInfo(_S):
    nominee_name: Optional[str] = None
    nominee_relation: Optional[str] = None
    nominee_percent: Optional[float] = None


class NFTContactInfo(_S):
    email: Optional[str] = None
    mobile: Optional[str] = None


class _NFTBase(_S):
    user_id: str
    member_code: str
    password: str
    amc: str
    rta: Literal["kfin", "cams"]
    member_id: str
    client_code: str
    entity_type: Optional[str] = None
    ref_id: Optional[str] = None


class NFTBankAccountChangeRequest(_NFTBase):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "user_id": "92374",
        "member_code": "92374",
        "password": "your-password",
        "amc": "SBI",
        "rta": "cams",
        "member_id": "92374",
        "client_code": "DematUCCTest1",
        "bank_change_info": [{"old_acc_no": "1234567890", "new_ifsc": "HDFC0002729",
                               "new_acc_no": "50100178851121", "new_acc_type": "SB"}],
    }})
    bank_change_info: List[NFTBankChangeInfo]


class NFTNomineeChangeRequest(_NFTBase):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "user_id": "92374",
        "member_code": "92374",
        "password": "your-password",
        "amc": "SBI",
        "rta": "cams",
        "member_id": "92374",
        "client_code": "DematUCCTest1",
        "nominee_change_info": [{"nominee_name": "Jane Doe",
                                  "nominee_relation": "SPOUSE", "nominee_percent": 100}],
    }})
    nominee_change_info: List[NFTNomineeInfo]


class NFTContactChangeRequest(_NFTBase):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "user_id": "92374",
        "member_code": "92374",
        "password": "your-password",
        "amc": "SBI",
        "rta": "cams",
        "member_id": "92374",
        "client_code": "DematUCCTest1",
        "contact_info": [{"email": "investor@example.com", "mobile": "9403231688"}],
    }})
    contact_info: List[NFTContactInfo]
