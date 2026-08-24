from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_validator


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
    modified_at: str = ""
    modified_till: str = ""


class SchemeSearch(BaseModel):
    value: str = ""


class SchemeMasterListRequest(BaseModel):
    """Optional filters for BSE's master scheme list."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "fields": ["ALL"],
                "count_only": False,
                "start": 0,
                "length": 20,
                "filter_param": {
                    "modified_at": "2026-06-20",
                    "modified_till": "2026-06-24",
                },
                "search": {"value": "PRTFGP-GR"},
            }
        }
    )

    fields: List[str] | None = Field(
        default=None,
        examples=[["ALL"]],
        description="Optional BSE field selector. Use ['ALL'] to request all available fields.",
    )
    count_only: bool = False
    start: int = 0
    length: int = 100
    filter_param: SchemeFilterParam | None = None
    search: SchemeSearch | None = None

    @field_validator("fields")
    @classmethod
    def reject_swagger_placeholder(cls, fields: List[str] | None) -> List[str] | None:
        if fields and any(field.strip().lower() == "string" for field in fields):
            raise ValueError("'string' is Swagger's placeholder, not a valid BSE field selector. Omit fields or use ['ALL'].")
        return fields
