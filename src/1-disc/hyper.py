from __future__ import annotations

import traceback
from hyperliquid.info import Info
from hyperliquid.utils import constants

import sys
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "hyper"

def utc_now()-> str:
    return datetime.now(timezone.utc).isoformat()

def write_json_atomic(path:Path,data:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w",encoding="utf-8") as f :
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
            default=str,
        )
        f.write("\n")
        '''save to json'''
    tmp_path.replace(path)


def main()-> int:
    try:
        info = Info(
            constants.MAINNET_API_URL,
            skip_ws=True,
        )

        meta, contexts = info.meta_and_asset_ctxs()
        fetched_at = utc_now()
        '''
        snapshot of meta and contexts
        '''
        meta_snapshot = {
            "schema_version": 1,
            "source": "hyperliquid",
            "endpoint": "meta_and_asset_ctxs",
            "fetched_at": fetched_at,
            "data": meta,
        }

        contexts_snapshot = {
            "schema_version": 1,
            "source": "hyperliquid",
            "endpoint": "meta_and_asset_ctxs",
            "fetched_at": fetched_at,
            "data": contexts,
        }

        write_json_atomic(
            DATA_DIR / "meta.json",
            meta_snapshot,
        )

        write_json_atomic(
            DATA_DIR / "asset_contexts.json",
            contexts_snapshot,
        )

        print(
            f"[hyper] snapshot saved "
            f"({len(contexts)} asset contexts)"
        )
        return 0

    except Exception as exc:
        print(
            f"[hyper] discovery failed:"
            f"{type(exc).__name__}:{exc}",
            file=sys.stderr,
        ) 
        traceback.print_exc()
        return 1

if __name__=="__main__":
    raise SystemExit(main())
