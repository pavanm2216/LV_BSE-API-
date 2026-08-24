from fastapi import APIRouter, Depends

from app.clients.starmf_client import StarMFClient
from app.dependencies import get_client
from app.schemas.sxp import (
    SXPCancelRequest,
    SXPGetHistoryRequest,
    SXPGetRequest,
    SXPListRequest,
    SXPPauseRequest,
    SXPRegisterRequest,
    SXPResumeRequest,
    SXPTopupRequest,
)

router = APIRouter(prefix="/sxp", tags=["SXP (SIP/SWP/STP)"])


@router.post("/register")
async def sxp_register(payload: SXPRegisterRequest, client: StarMFClient = Depends(get_client)):
    """Register a SIP, XSIP, SWP, or STP — set sxp_type accordingly."""
    return await client.post("v2/sxp_register", payload.model_dump(exclude_none=True))


@router.post("/cancel")
async def sxp_cancel(payload: SXPCancelRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("v2/sxp_cancel", payload.model_dump(exclude_none=True))


@router.post("/pause")
async def sxp_pause(payload: SXPPauseRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("v2/sxp_set_pause", payload.model_dump(exclude_none=True))


@router.post("/resume")
async def sxp_resume(payload: SXPResumeRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("v2/sxp_resume", payload.model_dump(exclude_none=True))


@router.post("/get")
async def sxp_get(payload: SXPGetRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("v2/sxp_get", payload.model_dump(exclude_none=True))


@router.post("/topup")
async def sxp_topup(payload: SXPTopupRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("v2/sxp_topup", payload.model_dump(exclude_none=True))


@router.post("/history")
async def sxp_get_history(payload: SXPGetHistoryRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("v2/sxp_get_history", payload.model_dump(exclude_none=True))


@router.post("/list")
async def sxp_list(payload: SXPListRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("v2/sxp_list", payload.model_dump(exclude_none=True))
