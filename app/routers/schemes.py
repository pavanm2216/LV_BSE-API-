from fastapi import APIRouter, Depends

from app.clients.starmf_client import StarMFClient
from app.dependencies import get_client
from app.schemas.schemes import SchemeMasterListRequest

router = APIRouter(prefix="/schemes", tags=["Schemes"])


@router.post("/master-list")
async def scheme_master_list(payload: SchemeMasterListRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("v2/master_scheme_list", payload.model_dump(exclude_none=True))
