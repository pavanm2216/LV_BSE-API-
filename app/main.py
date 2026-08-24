from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.security import HTTPBearer

from app.clients.starmf_client import StarMFClient
from app.config import get_settings
from app.routers import (
    login,
    kyc,
    mandate,
    nav,
    nft,
    orders,
    payment_detail,
    payment_gateway,
    schemes,
    sxp,
    twofa,
    ucc,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create all tables if they don't exist
    from app.db.database import Base, engine
    from app.db import models  # noqa: F401 — registers all models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    settings = get_settings()
    app.state.starmf_client = StarMFClient(settings)
    yield
    await app.state.starmf_client.aclose()


app = FastAPI(
    title="STARMF 2.0 Gateway",
    description=(
        "FastAPI wrapper over BSE STARMF 2.0 (Login, UCC, Orders, SXP, Schemes, "
        "KYC, Payment Detail, NFT, Mandate, NAV, 2FA, Payment Gateway). "
        "Proxies requests to the configured BSE StAR MF host, wraps bodies as "
        "{'data': ...}, and manages the bearer token after /login."
    ),
    version="0.1.0",
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True},
    openapi_tags=[
        {"name": "Login"},
        {"name": "UCC"},
        {"name": "Orders"},
        {"name": "SXP"},
        {"name": "Schemes"},
        {"name": "KYC"},
        {"name": "Payment Detail"},
        {"name": "NFT"},
        {"name": "Mandate"},
        {"name": "NAV"},
        {"name": "2FA"},
        {"name": "Payment Gateway"},
        {"name": "Meta"},
    ],
)

_bearer = HTTPBearer(auto_error=False)

app.include_router(login.router)
app.include_router(ucc.router)
app.include_router(orders.router)
app.include_router(sxp.router)
app.include_router(schemes.router)
app.include_router(kyc.router)
app.include_router(payment_detail.router)
app.include_router(nft.router)
app.include_router(mandate.router)
app.include_router(nav.router)
app.include_router(twofa.router)
app.include_router(payment_gateway.router)


@app.get("/healthz", tags=["Meta"])
async def healthz():
    return {"status": "ok"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    from fastapi.openapi.utils import get_openapi
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Paste the access_token from POST /login response",
        }
    }
    schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi


@app.get("/healthz/starmf", tags=["Meta"])
async def healthz_starmf():
    """Ping BSE host and report whether it returns JSON. Use to check IP whitelisting status."""
    import httpx
    from app.clients.starmf_client import _extract_html_hint
    settings = get_settings()
    url = f"{settings.root_url}/login"
    try:
        async with httpx.AsyncClient(timeout=10, verify=settings.verify_tls) as client:
            resp = await client.post(url, json={"data": {}},
                                     headers={"Content-Type": "application/json"})
        try:
            resp.json()
            return {"status": "reachable", "bse_status_code": resp.status_code, "json_response": True}
        except ValueError:
            hint = _extract_html_hint(resp.text)
            return {
                "status": "blocked",
                "bse_status_code": resp.status_code,
                "json_response": False,
                "likely_cause": "IP not whitelisted / BSE maintenance",
                "page_hint": hint,
            }
    except httpx.RequestError as exc:
        return {"status": "unreachable", "error": str(exc)}
