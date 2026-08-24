import asyncio, sys, os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import asyncpg

async def run():
    url = os.getenv("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
    conn = await asyncpg.connect(url, ssl="prefer")
    try:
        await conn.execute("SET search_path TO public;")
        for migration in sorted(Path("migrations").glob("*.sql")):
            await conn.execute(migration.read_text())
            print(f"Applied {migration.name}")
    except Exception as e:
        print(f"Error [{type(e).__name__}]: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await conn.close()

asyncio.run(run())
