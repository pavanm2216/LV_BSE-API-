from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class NAVFilterParam(BaseModel):
    model_config = ConfigDict(extra="ignore")
    bse_scheme_code: Optional[str] = None
    nav_date: Optional[str] = None


class NAVMasterListRequest(BaseModel):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {
        "fields": ["ALL"],
        "start": 0,
        "length": 50,
        "filter_param": {"nav_date": "2026-08-24"},
    }})
    fields: Optional[List[str]] = None
    count_only: Optional[bool] = None
    start: Optional[int] = 0
    length: Optional[int] = 50
    filter_param: Optional[NAVFilterParam] = None
