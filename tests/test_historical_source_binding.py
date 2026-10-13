"""Historical result identity does not waive current-source verification."""

import json
import shutil
from pathlib import Path

import pytest

from scripts import validate_results as evidence


@pytest.fixture
def source_tree(tmp_path, monkeypatch):
    root = evidence.ROOT
    raw = json.loads((root / "results/reference.json").read_text())
    names = list(raw["source"]["files"]) + [evidence._HISTORICAL_PATH, "results/reference.json"]
    for name in names:
        source = root / name
        if source.exists():
            target = tmp_path / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    monkeypatch.setattr(evidence, "ROOT", tmp_path)
    return tmp_path


def test_exact_historical_record_binds_original_archive(source_tree):
    report = evidence.validate(source_tree / "results/reference.json")
    assert report["source_scope"] == "historical_archived_core"
    assert report["samples"] == 5880
    assert report["archived_source_files"] == ["src/capprune/index.py"]


def test_modified_archive_fails(source_tree):
    archive = source_tree / evidence._HISTORICAL_PATH
    archive.write_bytes(archive.read_bytes() + b"\n")
    with pytest.raises(AssertionError, match="src/capprune/index.py"):
        evidence.validate(source_tree / "results/reference.json")


def test_relabelled_old_result_cannot_use_archive(source_tree):
    path = source_tree / "results/reference.json"
    raw = json.loads(path.read_text())
    raw["run_id"] = "a-new-run-id"
    path.write_text(json.dumps(raw))
    with pytest.raises(AssertionError, match="src/capprune/index.py"):
        evidence.validate(path)


def test_unarchived_historical_source_still_bound(source_tree):
    path = source_tree / "benchmark.py"
    path.write_bytes(path.read_bytes() + b"\n")
    with pytest.raises(AssertionError, match="benchmark.py"):
        evidence.validate(source_tree / "results/reference.json")


def test_new_protocol_keeps_old_input_seeds_and_tightens_scores():
    old = json.loads(Path("configs/protocol.json").read_text())
    new = json.loads(Path("configs/protocol-rowwise-20261013.json").read_text())
    assert new["cases"][: len(old["cases"])] == old["cases"]
    assert new["seed"] == old["seed"]
    assert new["correctness"]["score_atol"] == new["correctness"]["score_rtol"] == 0
    assert {500, 5000, 50000} <= {c["n"] for c in new["cases"] if c["kind"] == "clustered"}
