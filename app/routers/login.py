from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.starmf_client import StarMFClient
from app.db.database import get_db
from app.dependencies import get_client
from app.schemas.login import LoginRequest

router = APIRouter(prefix="", tags=["Login"])


@router.post("/login")
async def login(
    payload: LoginRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    """Authenticate against STARMF and cache the access_token for subsequent calls."""
    return await client.login(payload.username, payload.password, db=db)
