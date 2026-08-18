import asyncio, sys, os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def test():
    url = os.getenv("DATABASE_URL")
    print("Testing:", url)
    for ssl in ["require", "prefer", "disable", None]:
        try:
            kw = {"connect_args": {"ssl": ssl}} if ssl else {}
            engine = create_async_engine(url, **kw)
            async with engine.connect() as conn:
                v = await conn.execute(text("SELECT version()"))
                print(f"ssl={ssl} -> Connected: {v.scalar()}")
            await engine.dispose()
            return
        except Exception as e:
            print(f"ssl={ssl} -> [{type(e).__name__}]: {e}", file=sys.stderr)

asyncio.run(test())
