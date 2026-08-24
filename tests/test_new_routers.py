"""
Smoke tests for the 8 new routers added in the second pass.

Each test verifies:
  1. The correct BSE path is called.
  2. The request body is wrapped as {"data": ...}.
  3. Authorization: Bearer <token> is attached.
  4. A 4xx from BSE propagates as an HTTPException with the same status code.

Uses respx to mock the BSE HTTP layer so no real network calls are made.
"""
from __future__ import annotations

import pytest
import respx
from fastapi.testclient import TestClient
from httpx import Response

from app.config import get_settings
from app.main import app

BSE_BASE = "https://www.example-starmf-host.com"
TOKEN = "test-token-abc"


@pytest.fixture(autouse=True)
def _patch_settings():
    """Override get_settings cache so the lifespan client uses our test URL."""
    # The client is created during lifespan from get_settings(); we patch the
    # cached singleton so TestClient's lifespan picks up the test base_url.
    get_settings.cache_clear()
    import os
    os.environ.setdefault("STARMF_BASE_URL", "www.example-starmf-host.com")
    yield
    get_settings.cache_clear()


@pytest.fixture()
def authed_client():
    """TestClient with a pre-seeded bearer token on the shared StarMFClient."""
    with TestClient(app) as c:
        app.state.starmf_client.set_token(TOKEN)
        yield c


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _ok(body: dict | list = None):
    return Response(200, json={"status": "success", "data": body or {}})


def _assert_envelope(request, expected_data: dict | list):
    """Confirm the outgoing body is {"data": expected_data}."""
    assert request.content  # not empty
    import json
    sent = json.loads(request.content)
    assert sent == {"data": expected_data}


def _assert_bearer(request):
    assert request.headers.get("authorization") == f"Bearer {TOKEN}"


# ---------------------------------------------------------------------------
# 1. Schemes — POST /schemes/master-list  →  BSE master_scheme_list
# ---------------------------------------------------------------------------

@respx.mock
def test_scheme_master_list(authed_client):
    route = respx.post(f"{BSE_BASE}/master_scheme_list").mock(return_value=_ok())
    resp = authed_client.post("/schemes/master-list", json={"start": 0, "length": 10})
    assert resp.status_code == 200
    _assert_bearer(route.calls[0].request)
    _assert_envelope(route.calls[0].request, {"start": 0, "length": 10})


@respx.mock
def test_scheme_master_list_omits_empty_defaults(authed_client):
    route = respx.post(f"{BSE_BASE}/master_scheme_list").mock(return_value=_ok())
    resp = authed_client.post("/schemes/master-list", json={})
    assert resp.status_code == 200
    _assert_envelope(route.calls[0].request, {"start": 0, "length": 100})


def test_scheme_master_list_rejects_swagger_field_placeholder(authed_client):
    resp = authed_client.post("/schemes/master-list", json={"fields": ["string"]})
    assert resp.status_code == 422


@respx.mock
def test_scheme_master_list_forwards_modified_date_filters(authed_client):
    route = respx.post(f"{BSE_BASE}/master_scheme_list").mock(return_value=_ok())
    payload = {
        "fields": ["ALL"],
        "start": 0,
        "length": 20,
        "filter_param": {"modified_at": "2026-06-20", "modified_till": "2026-06-24"},
        "search": {"value": "PRTFGP-GR"},
    }
    resp = authed_client.post("/schemes/master-list", json=payload)
    assert resp.status_code == 200
    _assert_envelope(route.calls[0].request, payload)


# ---------------------------------------------------------------------------
# 2. KYC — POST /kyc/link  →  BSE v2/get_kyc_link
# ---------------------------------------------------------------------------

@respx.mock
def test_kyc_link(authed_client):
    route = respx.post(f"{BSE_BASE}/v2/get_kyc_link").mock(return_value=_ok())
    payload = {"items": [{"event": "ucc_kyc_pending", "member_code": "M001"}]}
    resp = authed_client.post("/kyc/link", json=payload)
    assert resp.status_code == 200
    _assert_bearer(route.calls[0].request)
    _assert_envelope(route.calls[0].request, [{"event": "ucc_kyc_pending", "member_code": "M001"}])


# ---------------------------------------------------------------------------
# 3. Payment Detail — POST /payment-detail/get  →  BSE get_payment_detail
# ---------------------------------------------------------------------------

@respx.mock
def test_payment_detail_get(authed_client):
    route = respx.post(f"{BSE_BASE}/get_payment_detail").mock(return_value=_ok())
    resp = authed_client.post("/payment-detail/get", json={"order_id": "ORD123"})
    assert resp.status_code == 200
    _assert_bearer(route.calls[0].request)
    _assert_envelope(route.calls[0].request, {"order_id": "ORD123"})


# ---------------------------------------------------------------------------
# 4. NFT — POST /nft/bank-account-change  →  BSE nft_bank_account_change
# ---------------------------------------------------------------------------

@respx.mock
def test_nft_bank_account_change(authed_client):
    route = respx.post(f"{BSE_BASE}/nft_bank_account_change").mock(return_value=_ok())
    payload = {
        "user_id": "U1", "member_code": "M1", "password": "pw",
        "amc": "AMC1", "rta": "kfin", "member_id": "MID1", "client_code": "CC1",
        "bank_change_info": [{"amc_code": "AMC1", "folio_no": "F001"}],
    }
    resp = authed_client.post("/nft/bank-account-change", json=payload)
    assert resp.status_code == 200
    _assert_bearer(route.calls[0].request)


# ---------------------------------------------------------------------------
# 5. Mandate — POST /mandate/get  →  BSE mandate_get
# ---------------------------------------------------------------------------

@respx.mock
def test_mandate_get(authed_client):
    route = respx.post(f"{BSE_BASE}/mandate_get").mock(return_value=_ok())
    resp = authed_client.post("/mandate/get", json={"exch_mandate_id": "MND001"})
    assert resp.status_code == 200
    _assert_bearer(route.calls[0].request)
    _assert_envelope(route.calls[0].request, {"exch_mandate_id": "MND001"})


# ---------------------------------------------------------------------------
# 6. NAV — POST /nav/master-list  →  BSE nav_master_list
# ---------------------------------------------------------------------------

@respx.mock
def test_nav_master_list(authed_client):
    route = respx.post(f"{BSE_BASE}/nav_master_list").mock(return_value=_ok())
    resp = authed_client.post("/nav/master-list", json={"filter_param": {"nav_date": "23-Oct-2025"}})
    assert resp.status_code == 200
    _assert_bearer(route.calls[0].request)
    _assert_envelope(route.calls[0].request, {"start": 0, "length": 50, "filter_param": {"nav_date": "23-Oct-2025"}})


# ---------------------------------------------------------------------------
# 7. 2FA — POST /2fa/get-link  →  BSE v2/get_2fa_link
# ---------------------------------------------------------------------------

@respx.mock
def test_twofa_get_link(authed_client):
    route = respx.post(f"{BSE_BASE}/v2/get_2fa_link").mock(return_value=_ok())
    payload = {"items": [{"event": "verify_order_cancel", "order": "ORD999"}]}
    resp = authed_client.post("/2fa/get-link", json=payload)
    assert resp.status_code == 200
    _assert_bearer(route.calls[0].request)
    _assert_envelope(route.calls[0].request, [{"event": "verify_order_cancel", "order": "ORD999"}])


# ---------------------------------------------------------------------------
# 8. Payment Gateway — POST /payment-gateway/status  →  BSE get_bse_pg_payment_status
# ---------------------------------------------------------------------------

@respx.mock
def test_payment_gateway_status(authed_client):
    route = respx.post(f"{BSE_BASE}/get_bse_pg_payment_status").mock(return_value=_ok())
    resp = authed_client.post("/payment-gateway/status", json={"order_id": "ORD123"})
    assert resp.status_code == 200
    _assert_bearer(route.calls[0].request)
    _assert_envelope(route.calls[0].request, {"order_id": "ORD123"})


# ---------------------------------------------------------------------------
# Error propagation — BSE 4xx becomes HTTPException with same status
# ---------------------------------------------------------------------------

@respx.mock
def test_upstream_error_propagates(authed_client):
    respx.post(f"{BSE_BASE}/nav_master_list").mock(
        return_value=Response(422, json={"detail": "invalid filter"})
    )
    resp = authed_client.post("/nav/master-list", json={})
    assert resp.status_code == 422
