"""Validate raw evidence and relevant source fingerprints. / 验证原始证据与相关源码指纹。"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Exact historical record only: never waive source checks for arbitrary old runs.
# 仅接受这份原始记录的精确归档，不为任意旧结果免除源码检查。
_HISTORICAL_RAW = "b46e739d31ff174ce9c9fb09f22819f1c7822f2235fbbeaf07a161cd82aacb08"
_HISTORICAL_CORE = "ab0afbaa8ee3d63efc43266b8bee249c00514a41ee8fe19f53088d3ebb850aad"
_HISTORICAL_PATH = "research/historical/20260921/index.py.source"


def validate(path: Path) -> dict:
    raw_bytes = path.read_bytes()
    raw = json.loads(raw_bytes)
    historical = hashlib.sha256(raw_bytes).hexdigest() == _HISTORICAL_RAW
    archived = []
    assert raw["schema_version"] == 1
    assert raw["status"] == "passed", "Recorded failures / 存在失败记录"
    assert raw["run_id"] and raw["started_at"] and raw["finished_at"]
    protocol = raw["protocol"]
    assert len(raw["cases"]) == len(protocol["cases"])
    assert all(v == "1" for v in raw["environment"]["requested_thread_environment"].values())
    count = 0
    for case in raw["cases"]:
        assert case["status"] == "passed" and case["correctness"]["all_passed"]
        expected = protocol["queries_per_case"] * protocol["repetitions"] * len(protocol["modes"])
        assert len(case["samples"]) == expected
        keys = {(s["repeat"], s["query_id"], s["mode"]) for s in case["samples"]}
        assert keys == {
            (r, q, m)
            for r in range(protocol["repetitions"])
            for q in range(protocol["queries_per_case"])
            for m in protocol["modes"]
        }
        for sample in case["samples"]:
            assert sample["elapsed_ns"] > 0
            assert sample["ids_equal"] and sample["scores_close"]
            assert 0 < sample["evaluated_vectors"] <= case["actual_shape"][0]
        count += expected
    for name, digest in raw["source"]["files"].items():
        if name.startswith(("src/", "configs/")) or name in {
            "benchmark.py",
            "scripts/evidence.py",
            "configs/protocol.json",
            "uv.lock",
            "pyproject.toml",
        }:
            checked = ROOT / name
            if historical and name == "src/capprune/index.py":
                assert digest == _HISTORICAL_CORE, "Historical core identity changed"
                checked = ROOT / _HISTORICAL_PATH
                archived.append(name)
            assert hashlib.sha256(checked.read_bytes()).hexdigest() == digest, name
    return {
        "cases": len(raw["cases"]),
        "samples": count,
        "run_id": raw["run_id"],
        "source_scope": "historical_archived_core" if archived else "current_tree",
        "archived_source_files": archived,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    print(json.dumps(validate(args.path)))


if __name__ == "__main__":
    main()
