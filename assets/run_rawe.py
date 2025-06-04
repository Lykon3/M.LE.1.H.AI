# run_rawe.py
from core.unified_arbitrage_system import run_unified_arbitrage

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_unified_arbitrage())