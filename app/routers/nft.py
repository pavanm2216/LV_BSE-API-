from fastapi import APIRouter, Depends

from app.clients.starmf_client import StarMFClient
from app.dependencies import get_client
from app.schemas.nft import NFTBankAccountChangeRequest, NFTContactChangeRequest, NFTNomineeChangeRequest

router = APIRouter(prefix="/nft", tags=["NFT"])


@router.post("/bank-account-change")
async def nft_bank_account_change(payload: NFTBankAccountChangeRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("nft_bank_account_change", payload.model_dump(exclude_none=True))


@router.post("/nominee-change")
async def nft_nominee_change(payload: NFTNomineeChangeRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("nft_nominee_change", payload.model_dump(exclude_none=True))


@router.post("/contact-change")
async def nft_contact_change(payload: NFTContactChangeRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("nft_contact_change", payload.model_dump(exclude_none=True))
