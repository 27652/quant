from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from hyperliquid.info import Info
from hyperliquid.utils import constants

from disc.hyper import fetch_snapshot


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "raw" / "hyperliquid"

INTERVAL_SECONDS = 5


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as f:
        json.dump(
            record,
            f,
            ensure_ascii=False,
        )
        f.write("\n")


def main() -> int:
    info = Info(
        constants.MAINNET_API_URL,
        skip_ws=True,
    )

    try:
        while True:
            started = time.monotonic()

            snapshot = fetch_snapshot(info)

            date = snapshot["fetched_at"][:10]
            output_path = DATA_DIR / f"{date}.jsonl"

            append_jsonl(
                output_path,
                snapshot,
            )

            print(
                f'{snapshot["fetched_at"]} '
                f'{len(snapshot["contexts"])} assets'
            )

            elapsed = time.monotonic() - started
            time.sleep(
                max(0, INTERVAL_SECONDS - elapsed)
            )

    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())