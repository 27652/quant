from __future__ import annotations

import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import traceback

from polymarket import AsyncPublicClient


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" /"meta" /"polymarket"

KEYWORDS=(
    "bitcoin",
    "btc",
    "eth",
    "ethereum",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def series_to_record(
    series: Any,
    fetched_at: str,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "source": "polymarket",
        "fetched_at": fetched_at,
        "id": str(series.id),
        "title": series.title,
        "slug": series.slug,
    }

def write_jsonl_atomic(
    path: Path,
    records: list[dict[str, Any]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    tmp_path = path.with_suffix(path.suffix + ".tmp")

    with tmp_path.open("w", encoding="utf-8") as f:
        for record in records:
            json.dump(
                record,
                f,
                ensure_ascii=False,
            )
            f.write("\n")

    tmp_path.replace(path)


def is_relevant(title: str, slug: str) -> bool:
    text = f"{title} {slug}".lower()
    return any(keyword in text for keyword in KEYWORDS)



async def disc_mar()->list[dict[str,Any]]:
    records: list[dict[str,Any]]=[]
    async with AsyncPublicClient() as client:
        raw_path = DATA_DIR / "series.txt"
        raw_path.parent.mkdir(parents=True, exist_ok=True)

        with open(raw_path,"w",encoding="utf-8") as f:
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
                title = series.title or ""
                slug=series.slug or ""

                if not is_relevant(title,slug):
                    continue
                records.append(
                    series_to_record(
                        series,
                        fetched_at=utc_now(),
                    )
                )
    return records
async def main() -> int:
    try:
        records = await disc_mar()

        output_path = DATA_DIR / "filtered_series.jsonl"

        write_jsonl_atomic(
            output_path,
            records,
        )

        print(
            f"[polymarket] saved "
            f"{len(records)} relevant series"
        )

        return 0

    except Exception as exc:
        print(
            f"[polymarket] discovery failed: "
            f"{type(exc).__name__}: {exc}",
            file=sys.stderr,
        )

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))




