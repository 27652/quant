import dataclasses
import decimal
from polymarket import AsyncPublicClient
import asyncio

keywords=(
    "bitcoin",
    "btc",
    "eth",
    "ethereum",
)

async def disc_mar():
    async with AsyncPublicClient() as client:

        with open("./data/polymarket/series.csv","w",encoding="utf-8") as f:
            async for series in client.list_series(
                closed=False,
                page_size=50,
            ).iter_items():

                print(
                    series.id,
                    series.title,
                    series.slug,
                    file=f,
                )
asyncio.run(disc_mar())





