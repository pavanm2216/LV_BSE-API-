from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.starmf_client import StarMFClient
from app.db.database import get_db
from app.db.models import BseUcc
from app.dependencies import get_client
from app.schemas.ucc import (
    AddUCCRequest,
    DeactivateUCCRequest,
    GetUCCRequest,
    ListUCCRequest,
    UpdateUCCRequest,
    UpdateUCCStatusRequest,
    UpdateUCCProfileRequest,
    UpdateUCCBankRequest,
    UpdateUCCPersonRequest,
    UpdateUCCNomineeRequest,
    UpdateUCCFatcaRequest,
    UpdateUCCCommAddrRequest,
    UpdateUCCForeignAddrRequest,
    UpdateUCCDepositoryRequest,
    UpdateUCCContactRequest,
    UpdateUCCIdentifierRequest,
    UpdateUCCHoldingNatureRequest,
    UpdateUCCHolderObjectRequest,
)

router = APIRouter(prefix="/ucc", tags=["UCC"])

BSE_UPDATE_PATH = "v2/update_ucc"


async def _persist_and_call(payload: dict, bse_path: str, client: StarMFClient, db: AsyncSession):
    """Save to DB, call BSE, update DB with result."""
    ucc = BseUcc(
        request_client_code=(payload.get("investor") or {}).get("client_code"),
        request_payload=payload,
        submission_status="SUBMITTING",
    )
    db.add(ucc)
    await db.commit()

    try:
        result = await client.post(bse_path, payload)
    except HTTPException as exc:
        ucc.submission_status = "FAILED"
        ucc.failure_detail = jsonable_encoder(
            exc.detail if isinstance(exc.detail, (dict, list)) else {"detail": str(exc.detail)}
        )
        await db.commit()
        raise

    bse_data = result.get("data") or {}
    bse_status = bse_data.get("status") or ""
    ucc.submission_status = "APPROVED" if bse_status == "APPROVED" else "SUCCESS"
    ucc.bse_client_code = bse_data.get("client_code")
    ucc.member_code = bse_data.get("member_code")
    ucc.bse_ucc_status = bse_status
    ucc.response_payload = jsonable_encoder(result)
    await db.commit()
    return result


# ---------------------------------------------------------------------------
# Add UCC
# ---------------------------------------------------------------------------

@router.post("/add", response_model=Dict[str, Any])
async def add_ucc(
    payload: AddUCCRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    request_payload = payload.model_dump(exclude_none=True, mode="json")

    primary_holder = next((h for h in (request_payload.get("holder") or []) if str(h.get("holder_rank")) == "1"), {})
    person = primary_holder.get("person") or {}
    primary_contact = next(iter(primary_holder.get("contact") or []), {})
    pan_id = next((i for i in (primary_holder.get("identifier") or []) if i.get("identifier_type") == "pan"), {})
    comm_addr = request_payload.get("comm_addr") or {}
    primary_bank = next(iter(request_payload.get("bank_account") or []), {})

    ucc = BseUcc(
        request_client_code=(request_payload.get("investor") or {}).get("client_code"),
        request_payload=request_payload,
        holding_nature=request_payload.get("holding_nature"),
        tax_status=request_payload.get("tax_status"),
        tax_code=request_payload.get("tax_code"),
        rdmp_idcw_pay_mode=request_payload.get("rdmp_idcw_pay_mode"),
        is_client_physical=request_payload.get("is_client_physical"),
        is_client_demat=request_payload.get("is_client_demat"),
        is_nomination_opted=request_payload.get("is_nomination_opted"),
        comm_mode=request_payload.get("comm_mode"),
        onboarding=request_payload.get("onboarding"),
        is_multi_ucc=request_payload.get("is_multi_ucc"),
        parent_client_code=request_payload.get("parent_client_code"),
        primary_pan=pan_id.get("identifier_number"),
        primary_first_name=person.get("first_name"),
        primary_last_name=person.get("last_name"),
        primary_dob=person.get("dob"),
        primary_gender=person.get("gender"),
        primary_email=primary_contact.get("email_address"),
        primary_mobile=primary_contact.get("contact_number"),
        kyc_type=primary_holder.get("kyc_type"),
        comm_address_line_1=comm_addr.get("address_line_1"),
        comm_city=comm_addr.get("City"),
        comm_state=comm_addr.get("state"),
        comm_postalcode=comm_addr.get("postalcode"),
        comm_country=comm_addr.get("country"),
        bank_ifsc=primary_bank.get("ifsc_code"),
        bank_acc_num=primary_bank.get("bank_acc_num"),
        bank_acc_type=primary_bank.get("bank_acc_type"),
    )
    db.add(ucc)
    await db.commit()

    try:
        result = await client.post("v2/add_ucc", request_payload)
    except HTTPException as exc:
        ucc.submission_status = "FAILED"
        ucc.failure_detail = jsonable_encoder(
            exc.detail if isinstance(exc.detail, (dict, list)) else {"detail": str(exc.detail)}
        )
        await db.commit()
        raise

    bse_data = result.get("data") or {}
    bse_status = bse_data.get("status") or ""
    ucc.submission_status = "APPROVED" if bse_status == "APPROVED" else "SUCCESS"
    ucc.bse_client_code = bse_data.get("client_code")
    ucc.member_code = bse_data.get("member_code")
    ucc.bse_ucc_status = bse_status
    ucc.response_payload = jsonable_encoder(result)
    await db.commit()
    return result


# ---------------------------------------------------------------------------
# Update UCC — dedicated endpoint per BSE sub-type
# ---------------------------------------------------------------------------

@router.post("/update/status", response_model=Dict[str, Any], summary="update_ucc() Individual UCC status")
async def update_ucc_status(
    payload: UpdateUCCStatusRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


@router.post("/update/profile", response_model=Dict[str, Any], summary="update_ucc() Profile (Holding Nature, Holder and FATCA)")
async def update_ucc_profile(
    payload: UpdateUCCProfileRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


@router.post("/update/bank", response_model=Dict[str, Any], summary="update_ucc() Bank Account")
async def update_ucc_bank(
    payload: UpdateUCCBankRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


@router.post("/update/person", response_model=Dict[str, Any], summary="update_ucc() person")
async def update_ucc_person(
    payload: UpdateUCCPersonRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


@router.post("/update/nominee", response_model=Dict[str, Any], summary="update_ucc() Nominee")
async def update_ucc_nominee(
    payload: UpdateUCCNomineeRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


@router.post("/update/fatca", response_model=Dict[str, Any], summary="update_ucc() FATCA")
async def update_ucc_fatca(
    payload: UpdateUCCFatcaRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


@router.post("/update/comm-addr", response_model=Dict[str, Any], summary="update_ucc() Communication Address")
async def update_ucc_comm_addr(
    payload: UpdateUCCCommAddrRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


@router.post("/update/foreign-addr", response_model=Dict[str, Any], summary="update_ucc() Foreign Address")
async def update_ucc_foreign_addr(
    payload: UpdateUCCForeignAddrRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


@router.post("/update/depository", response_model=Dict[str, Any], summary="update_ucc() DP Details")
async def update_ucc_depository(
    payload: UpdateUCCDepositoryRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


@router.post("/update/contact", response_model=Dict[str, Any], summary="update_ucc() Contact Details")
async def update_ucc_contact(
    payload: UpdateUCCContactRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


@router.post("/update/identifier", response_model=Dict[str, Any], summary="update_ucc() Identifier Details")
async def update_ucc_identifier(
    payload: UpdateUCCIdentifierRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


@router.post("/update/holding-nature", response_model=Dict[str, Any], summary="update_ucc() Holding Nature SI to JO")
async def update_ucc_holding_nature(
    payload: UpdateUCCHoldingNatureRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


@router.post("/update/holder", response_model=Dict[str, Any], summary="update_ucc() Update UCC Holder Object")
async def update_ucc_holder_object(
    payload: UpdateUCCHolderObjectRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


# ---------------------------------------------------------------------------
# Generic update (backward compat) + Deactivate
# ---------------------------------------------------------------------------

@router.post("/update", response_model=Dict[str, Any])
async def update_ucc(
    payload: UpdateUCCRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


@router.post("/deactivate", response_model=Dict[str, Any], summary="deactivate_ucc")
async def deactivate_ucc(
    payload: DeactivateUCCRequest,
    client: StarMFClient = Depends(get_client),
    db: AsyncSession = Depends(get_db),
):
    return await _persist_and_call(
        payload.model_dump(exclude_none=True, mode="json"), BSE_UPDATE_PATH, client, db
    )


# ---------------------------------------------------------------------------
# Get / List
# ---------------------------------------------------------------------------

@router.post("/get", response_model=Dict[str, Any])
async def get_ucc(payload: GetUCCRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("v2/get_ucc", payload.model_dump(exclude_none=True, mode="json"))


@router.post("/list", response_model=Dict[str, Any])
async def list_ucc(payload: ListUCCRequest, client: StarMFClient = Depends(get_client)):
    data = payload.model_dump(exclude_none=True, mode="json")
    # BSE requires these keys present even when empty
    data.setdefault("member", {})
    data.setdefault("investor", {})
    data.setdefault("filter_param", {})
    # Strip empty investor sub-fields (Swagger placeholders like "string" break BSE)
    inv = data.get("investor") or {}
    data["investor"] = {k: v for k, v in inv.items() if v and v != "string"}
    # Strip filter_param placeholder strings
    fp = data.get("filter_param") or {}
    data["filter_param"] = {k: v for k, v in fp.items() if v is not None and v != "string"}
    # Strip fields placeholder
    if data.get("fields") == ["string"]:
        data["fields"] = ["ALL"]
    return await client.post("v2/list_ucc", data)
