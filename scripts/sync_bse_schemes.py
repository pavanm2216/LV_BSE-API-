"""
Sync BSE scheme master data into LV_BSE database.
Usage: python scripts/sync_bse_schemes.py
"""
import asyncio, os, sys, uuid
from dotenv import load_dotenv
load_dotenv()

import httpx
import asyncpg


HOST     = os.getenv("STARMF_BASE_URL", "starmfv2demo.bseindia.com/api")
PROTOCOL = os.getenv("STARMF_PROTOCOL", "https")
BASE_URL = f"{PROTOCOL}://{HOST}"
USERNAME = os.getenv("STARMF_LOGIN_USERNAME")
PASSWORD = os.getenv("STARMF_LOGIN_PASSWORD")
DB_URL   = os.getenv("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")


async def bse_login(client: httpx.AsyncClient) -> str:
    resp = await client.post(
        f"{BASE_URL}/login",
        json={"data": {"username": USERNAME, "password": PASSWORD}},
        headers={"Content-Type": "application/json"},
    )
    resp.raise_for_status()
    data = resp.json()
    token = (data.get("data") or {}).get("access_token")
    if not token:
        print("Login response:", data)
        raise RuntimeError("No access_token in login response")
    print(f"Logged in. Token: {token[:20]}...")
    return token


async def fetch_schemes(client: httpx.AsyncClient, token: str, start: int = 0, length: int = 500) -> dict:
    resp = await client.post(
        f"{BASE_URL}/master_scheme_list",
        json={"data": {"start": start, "length": length}},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
    )
    resp.raise_for_status()
    return resp.json()


async def sync(conn: asyncpg.Connection, schemes: list):
    inserted_amcs = 0
    inserted_schemes = 0

    for s in schemes:
        amc_code = s.get("amc_code") or s.get("AmcCode") or s.get("amc") or "UNKNOWN"
        amc_name = s.get("amc_name") or s.get("AmcName") or amc_code

        # Upsert AMC
        amc_id = await conn.fetchval("""
            INSERT INTO bse_amcs (id, amc_code, amc_name)
            VALUES ($1, $2, $3)
            ON CONFLICT (amc_code) DO UPDATE SET amc_name = EXCLUDED.amc_name
            RETURNING id
        """, uuid.uuid4(), amc_code, amc_name)
        inserted_amcs += 1

        scheme_code = (s.get("scheme_code") or s.get("SchemeCode") or s.get("bse_scheme_code") or "").strip()
        scheme_name = (s.get("scheme_name") or s.get("SchemeName") or scheme_code).strip()
        isin        = s.get("isin") or s.get("ISIN")
        category    = s.get("category") or s.get("Category") or s.get("scheme_type")
        status      = s.get("status") or s.get("Status") or "Active"

        if not scheme_code:
            continue

        # Upsert scheme
        await conn.execute("""
            INSERT INTO bse_schemes (id, scheme_code, amc_id, scheme_name, isin, category, status)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (scheme_code) DO UPDATE SET
                scheme_name = EXCLUDED.scheme_name,
                isin        = EXCLUDED.isin,
                category    = EXCLUDED.category,
                status      = EXCLUDED.status
        """, uuid.uuid4(), scheme_code, amc_id, scheme_name, isin, category, status)
        inserted_schemes += 1

    return inserted_amcs, inserted_schemes


async def main():
    print(f"Connecting to DB: {DB_URL[:50]}...")
    conn = await asyncpg.connect(DB_URL, ssl="prefer")

    async with httpx.AsyncClient(timeout=60, verify=False) as client:
        token = await bse_login(client)

        total_saved = 0
        start = 0
        length = 500

        while True:
            print(f"Fetching schemes start={start} length={length}...")
            result = await fetch_schemes(client, token, start=start, length=length)

            # Print raw keys to understand response structure
            if start == 0:
                print("Response keys:", list(result.keys()))
                data_sample = result.get("data") or result
                if isinstance(data_sample, list) and len(data_sample) > 0:
                    print("First record keys:", list(data_sample[0].keys()))
                elif isinstance(data_sample, dict):
                    print("Data keys:", list(data_sample.keys()))

            records = result.get("data") or []
            if isinstance(records, dict):
                records = records.get("data") or records.get("records") or []

            if not records:
                print("No more records.")
                break

            amcs, schemes = await sync(conn, records)
            total_saved += schemes
            print(f"  Saved {schemes} schemes, {amcs} AMC upserts. Total so far: {total_saved}")

            if len(records) < length:
                break
            start += length

    await conn.close()
    print(f"\nDone. Total schemes saved: {total_saved}")


asyncio.run(main())
