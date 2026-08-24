from __future__ import annotations

import pytest
from fastapi import HTTPException

from app.routers.ucc import add_ucc
from app.schemas.ucc import AddUCCRequest


class FakeSession:
    def __init__(self):
        self.records = []
        self.commits = 0

    def add(self, record):
        self.records.append(record)

    async def commit(self):
        self.commits += 1


class SuccessfulClient:
    async def post(self, path, data):
        assert path == "v2/add_ucc"
        assert data["investor"]["client_code"] == "LOCAL-UCC-1"
        return {
            "status": "success",
            "data": {
                "client_code": "BSE-UCC-1",
                "member_code": "MEM-1",
                "status": "PENDING_VERIFICATION",
            },
        }


class FailingClient:
    async def post(self, path, data):
        raise HTTPException(status_code=400, detail={"status": "error"})


def _payload():
    return AddUCCRequest(investor={"client_code": "LOCAL-UCC-1"})


@pytest.mark.asyncio
async def test_add_ucc_persists_successful_bse_submission():
    db = FakeSession()
    result = await add_ucc(_payload(), SuccessfulClient(), db)

    assert result["status"] == "success"
    assert db.commits == 2
    record = db.records[0]
    assert record.request_client_code == "LOCAL-UCC-1"
    assert record.bse_client_code == "BSE-UCC-1"
    assert record.member_code == "MEM-1"
    assert record.bse_ucc_status == "PENDING_VERIFICATION"
    assert record.submission_status == "SUCCESS"


@pytest.mark.asyncio
async def test_add_ucc_records_bse_failure():
    db = FakeSession()

    with pytest.raises(HTTPException, match="400"):
        await add_ucc(_payload(), FailingClient(), db)

    assert db.commits == 2
    record = db.records[0]
    assert record.submission_status == "FAILED"
    assert record.failure_detail == {"status": "error"}
