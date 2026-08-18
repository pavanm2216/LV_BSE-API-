from fastapi import APIRouter, Depends

from app.clients.starmf_client import StarMFClient
from app.dependencies import get_client
from app.schemas.nav import NAVMasterListRequest

router = APIRouter(prefix="/nav", tags=["NAV"])


@router.post("/master-list")
async def nav_master_list(payload: NAVMasterListRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("nav_master_list", payload.model_dump(exclude_none=True))
