from fastapi import APIRouter, Depends

from app.clients.starmf_client import StarMFClient
from app.dependencies import get_client
from app.schemas.mandate import (
    MandateCancelRequest,
    MandateDelinkRequest,
    MandateGetRequest,
    MandateLinkRequest,
    MandateListRequest,
    MandateRegisterRequest,
    MandateUpdateRequest,
)

router = APIRouter(prefix="/mandate", tags=["Mandate"])


@router.post("/register")
async def mandate_register(payload: MandateRegisterRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("mandate_register", payload.model_dump(exclude_none=True))


@router.post("/cancel")
async def mandate_cancel(payload: MandateCancelRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("mandate_cancel", payload.model_dump(exclude_none=True))


@router.post("/get")
async def mandate_get(payload: MandateGetRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("mandate_get", payload.model_dump(exclude_none=True))


@router.post("/list")
async def mandate_list(payload: MandateListRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("mandate_list", payload.model_dump(exclude_none=True))


@router.post("/update")
async def mandate_update(payload: MandateUpdateRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("mandate_update", payload.model_dump(exclude_none=True))


@router.post("/link")
async def mandate_link(payload: MandateLinkRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("link_mandate", payload.model_dump(exclude_none=True))


@router.post("/delink")
async def mandate_delink(payload: MandateDelinkRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("mandate_delink", payload.model_dump(exclude_none=True))
