from fastapi import APIRouter, Depends

from app.clients.starmf_client import StarMFClient
from app.dependencies import get_client
from app.schemas.twofa import TwoFALinkRequest

router = APIRouter(prefix="/2fa", tags=["2FA"])


@router.post("/get-link")
async def twofa_get_link(payload: TwoFALinkRequest, client: StarMFClient = Depends(get_client)):
    # BSE expects the list directly as the data value
    items = [item.model_dump(exclude_none=True) for item in payload.items]
    return await client.post("v2/get_2fa_link", items)
