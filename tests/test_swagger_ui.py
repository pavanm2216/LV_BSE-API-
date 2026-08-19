"""
Playwright tests for STARMF 2.0 FastAPI Swagger UI.
Tests every endpoint section is visible and /login can be executed.

Run:
    # Start the server first:
    uvicorn app.main:app --reload

    # Then run tests:
    pytest tests/test_swagger_ui.py --headed   (with browser visible)
    pytest tests/test_swagger_ui.py            (headless)
"""
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"
SWAGGER_URL = f"{BASE_URL}/docs"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "ignore_https_errors": True}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def open_swagger(page: Page):
    page.goto(SWAGGER_URL)
    page.wait_for_selector(".swagger-ui", timeout=10_000)


def expand_endpoint(page: Page, method: str, path: str):
    """Click on an endpoint row to expand it."""
    selector = f"[id*='{method.lower()}'][id*='{path.replace('/', '_')}']"
    btn = page.locator(f"[data-path='{path}'][data-method='{method.lower()}']").first
    if btn.count() == 0:
        # fallback: find by visible text
        btn = page.get_by_text(path, exact=True).first
    btn.click()
    page.wait_for_timeout(500)


# ---------------------------------------------------------------------------
# 1. Page loads and title is correct
# ---------------------------------------------------------------------------

def test_swagger_page_loads(page: Page):
    open_swagger(page)
    expect(page).to_have_title("STARMF 2.0 Gateway - Swagger UI")


# ---------------------------------------------------------------------------
# 2. All API sections/tags are visible
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tag", [
    "Login",
    "UCC",
    "Orders",
    "SXP (SIP/SWP/STP)",
    "Schemes",
    "KYC",
    "Payment Detail",
    "NFT",
    "Mandate",
    "NAV",
    "2FA",
    "Payment Gateway",
])
def test_api_tag_visible(page: Page, tag: str):
    open_swagger(page)
    expect(page.get_by_text(tag, exact=True).first).to_be_visible()


# ---------------------------------------------------------------------------
# 3. All endpoints are listed
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("endpoint", [
    "/login",
    "/ucc/add",
    "/ucc/update",
    "/ucc/deactivate",
    "/ucc/get",
    "/ucc/list",
    "/orders/new",
    "/orders/update",
    "/orders/list",
    "/orders/get",
    "/orders/cancel",
    "/sxp/register",
    "/sxp/cancel",
    "/sxp/pause",
    "/sxp/resume",
    "/sxp/get",
    "/sxp/topup",
    "/sxp/history",
    "/sxp/list",
    "/schemes/master-list",
    "/kyc/link",
    "/payment-detail/get",
    "/payment-detail/list",
    "/nft/bank-account-change",
    "/nft/nominee-change",
    "/nft/contact-change",
    "/mandate/register",
    "/mandate/cancel",
    "/mandate/get",
    "/mandate/list",
    "/mandate/update",
    "/mandate/link",
    "/mandate/delink",
    "/nav/master-list",
    "/2fa/get-link",
    "/payment-gateway/exchpg-service",
    "/payment-gateway/send-payment-info",
    "/payment-gateway/status",
])
def test_endpoint_listed(page: Page, endpoint: str):
    open_swagger(page)
    expect(page.get_by_text(endpoint, exact=True).first).to_be_visible()


# ---------------------------------------------------------------------------
# 4. /login endpoint — expand, fill, execute (expects 4xx since BSE unreachable)
# ---------------------------------------------------------------------------

def test_login_endpoint_expand_and_try(page: Page):
    open_swagger(page)

    # Click the /login POST row to expand
    page.locator("span.opblock-summary-path", has_text="/login").first.click()
    page.wait_for_timeout(800)

    # Click "Try it out"
    page.get_by_role("button", name="Try it out").first.click()
    page.wait_for_timeout(500)

    # Fill in the request body
    textarea = page.locator("textarea.body-param__text").first
    textarea.fill("")
    textarea.type('{"username": "test_member", "password": "test_password"}')

    # Click Execute
    page.get_by_role("button", name="Execute").first.click()
    page.wait_for_timeout(3000)

    # Verify a response was received (curl command appears)
    expect(page.locator(".curl-command").first).to_be_visible()


# ---------------------------------------------------------------------------
# 5. /healthz endpoint returns 200
# ---------------------------------------------------------------------------

def test_healthz(page: Page):
    resp = page.goto(f"{BASE_URL}/healthz")
    assert resp.status == 200


# ---------------------------------------------------------------------------
# 6. OpenAPI JSON schema is accessible
# ---------------------------------------------------------------------------

def test_openapi_json(page: Page):
    resp = page.goto(f"{BASE_URL}/openapi.json")
    assert resp.status == 200
    body = page.evaluate("() => document.body.innerText")
    assert "STARMF" in body
    assert "paths" in body


# ---------------------------------------------------------------------------
# 7. /schemes/master-list — expand and verify Try it out works
# ---------------------------------------------------------------------------

def test_schemes_master_list_expand(page: Page):
    open_swagger(page)
    page.get_by_role("button", name="POST /schemes/master-list Scheme Master List").first.click()
    page.wait_for_timeout(500)
    expect(page.get_by_role("button", name="Try it out").first).to_be_visible()


# ---------------------------------------------------------------------------
# 8. /nav/master-list — expand and verify Try it out works
# ---------------------------------------------------------------------------

def test_nav_master_list_expand(page: Page):
    open_swagger(page)
    page.get_by_role("button", name="POST /nav/master-list Nav Master List").first.click()
    page.wait_for_timeout(500)
    expect(page.get_by_role("button", name="Try it out").first).to_be_visible()
