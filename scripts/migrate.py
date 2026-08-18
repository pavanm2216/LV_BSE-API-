import asyncio, sys, os
from dotenv import load_dotenv
load_dotenv()
import asyncpg

async def run():
    url = os.getenv("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
    sql = open("migrations/001_initial_schema.sql").read()
    conn = await asyncpg.connect(url, ssl="prefer")
    try:
        await conn.execute("SET search_path TO public;")
        await conn.execute(sql)
        print("Migration applied successfully.")
    except Exception as e:
        print(f"Error [{type(e).__name__}]: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await conn.close()

asyncio.run(run())
