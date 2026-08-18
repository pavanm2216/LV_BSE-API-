from fastapi import APIRouter, Depends

from app.clients.starmf_client import StarMFClient
from app.dependencies import get_client
from app.schemas.kyc import KYCLinkRequest

router = APIRouter(prefix="/kyc", tags=["KYC"])


@router.post("/link")
async def kyc_get_link(payload: KYCLinkRequest, client: StarMFClient = Depends(get_client)):
    # BSE expects the list directly as the data value
    items = [item.model_dump(exclude_none=True) for item in payload.items]
    return await client.post("v2/get_kyc_link", items)
