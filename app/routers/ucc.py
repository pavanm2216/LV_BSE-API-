from fastapi import APIRouter, Depends

from app.clients.starmf_client import StarMFClient
from app.dependencies import get_client
from app.schemas.ucc import (
    AddUCCRequest,
    DeactivateUCCRequest,
    GetUCCRequest,
    ListUCCRequest,
    UpdateUCCRequest,
)

router = APIRouter(prefix="/ucc", tags=["UCC"])


@router.post("/add")
async def add_ucc(payload: AddUCCRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("add_ucc", payload.model_dump(exclude_none=True))


@router.post("/update")
async def update_ucc(payload: UpdateUCCRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("update_ucc", payload.model_dump(exclude_none=True))


@router.post("/deactivate")
async def deactivate_ucc(payload: DeactivateUCCRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("update_ucc", payload.model_dump(exclude_none=True))


@router.post("/get")
async def get_ucc(payload: GetUCCRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("get_ucc", payload.model_dump(exclude_none=True))


@router.post("/list")
async def list_ucc(payload: ListUCCRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("list_ucc", payload.model_dump(exclude_none=True))
