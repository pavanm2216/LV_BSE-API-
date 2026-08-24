from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field

from app.schemas.common import Pagination


class SchemeFilterParam(BaseModel):
    scheme_amc_name: str = ""
    scheme_category: str = ""
    scheme_sub_category: str = ""
    investment_mode: str = ""
    scheme_option: str = ""
    scheme_plan: str = ""
    scheme_isin: str = ""
    settlement_days: str = ""
    transaction_allowed: str = ""


class SchemeSearch(BaseModel):
    value: str = ""


class SchemeMasterListRequest(BaseModel):
    fields: List[str] = Field(default_factory=lambda: ["ALL"])
    count_only: bool = False
    start: int = 0
    length: int = 100
    filter_param: SchemeFilterParam = Field(default_factory=SchemeFilterParam)
    search: SchemeSearch = Field(default_factory=SchemeSearch)
