import asyncio, os
from dotenv import load_dotenv
load_dotenv()
import asyncpg

async def run():
    url = os.getenv("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")
    conn = await asyncpg.connect(url, ssl="prefer")
    rows = await conn.fetch("""
        SELECT tablename FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY tablename
    """)
    print(f"Tables created ({len(rows)}):")
    for r in rows:
        print(f"  ✓ {r['tablename']}")
    await conn.close()

asyncio.run(run())
