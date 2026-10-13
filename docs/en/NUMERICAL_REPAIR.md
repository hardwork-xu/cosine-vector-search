# Numerical repair and unmeasured performance boundary

[中文](../zh/NUMERICAL_REPAIR.md) · [Experiments](EXPERIMENTS.md)

## What changed on 2026-10-13

A legal 101×16 near-duplicate fixture (seed 4, perturbation 1e-15, k=10) returned different IDs in full-scan and block modes under NumPy 2.2.6. The pruning-disabled block path also differed, identifying candidate-score reduction order rather than pruning as the cause. This was a practical mode-agreement defect, not a refutation of the real-arithmetic cap theorem.

Both candidate-score paths now call `_score_rows`, using `np.einsum("ij,j->i", vectors, query, optimize=False)`. No score clipping, rounding or enlarged tolerance is used. Build-time clustering and conservative cap bounds retain their previous implementation. The core plus 20 new regression cases passed 69 tests on the inspected NumPy 2.2.6 environment. Tests cover near ties at five dimensions/three k values, exact duplicates, original-ID tie order, persistence and independent Python sorting. These tests do not certify every platform or establish performance.

## Exact source identities

- Historical numerical source: `ab0afbaa8ee3d63efc43266b8bee249c00514a41ee8fe19f53088d3ebb850aad`. Its exact bytes are retained at [index.py.source](../../research/historical/20260921/index.py.source), outside the importable package.
- Corrected numerical source at this repair: `28f7273416fd1d20c8062c2884167c2c0f39739f04e3fe2ee7a11b08940d7360`.
- New protocol: [protocol-rowwise-20261013.json](../../configs/protocol-rowwise-20261013.json), SHA-256 `05d85870354eb512e67099e374f26e5eba8bb00f0d5187ad429e37a2a50af295`.
- Original raw run `140ea5bb-9c95-4e8a-b2ab-17bcde0903ca` and [original protocol](../../configs/protocol.json) are unchanged. The 10.20× primary result and all negative historical results refer only to the former source.

The source validator accepts the archive only when the **whole original result-file hash**, original source path and recorded source hash match the registered historical record. Every other measured runtime/harness/protocol/dependency file still needs its exact recorded hash. A renamed/reformatted/modified old result cannot borrow this exception. New runs bind current source; archive integrity does not mark new code as historically measured.

## New measurement, not an inherited speedup

**Status: the corrected kernel has not yet been performance-measured.** The new comparator is exhaustive scoring through the same rowwise kernel; it is not the former optimized BLAS scan. The original 1.50× timing target and 30% scoring target are retained as new-run targets only. Correctness is tightened to identical scores (`atol=rtol=0`) and ordered IDs. No result is preclaimed. This does not establish superiority to native BLAS, Faiss or real embedding retrieval. A separately timed strong native/BLAS baseline is still missing; this protocol compares internally consistent B/C paths only.

All seven original workloads, their ordering and seeds remain; a 500×64 clustered case is appended. The three clustered collection sizes are 500/5,000/50,000 with d=64 and k=10; their seeds and cluster counts differ, so this is coverage rather than a controlled scaling law. The 50,000×128 and k=100 cases add dimension/output stress. Isotropic 50,000×64, real digits and tiny k=N remain adverse/boundary cases. Each case uses 40 queries, 7 repetitions, 4 warmup queries and all 3 modes (6,720 measured calls over 8 cases). Run measurements serially, with the same source, inputs and requested one-thread environment. Download/setup/build are outside query timings; build/save/load are separately recorded.

The digits case uses the bundled scikit-learn 1.7.2 `load_digits` raw 64 pixel features: 1,797 images split by seeded permutation into 40 query rows and 1,757 indexed rows. No model or network dataset fetch is needed after dependency installation. This is numeric similarity, not a semantic embedding or classification-quality baseline. Keep the [dataset and dependency attribution](../../NOTICE.md).

## Reproduction commands

Use uv 0.8.22 and the existing lockfile. Measurement imports NumPy 2.2.6, threadpoolctl 3.6.0, psutil 7.1.0 and scikit-learn 1.7.2 (SciPy transitive); analysis uses Matplotlib 3.10.6 and pyparsing 3.2.3. `uv sync --frozen` installs these development tools and exact locked dependencies. Do not replace the lockfile to simplify installation. If the global uv version differs, use `uvx --from uv==0.8.22 uv sync --frozen` without modifying the global executable. `PYTHONPATH=src` ensures this checkout's core is measured even when an older editable package is installed elsewhere.

```sh
# Python 3.12 and project-pinned uv / 使用Python 3.12和锁定uv
uv sync --frozen
PYTHONPATH=src .venv/bin/python -m pytest -q tests/test_core.py tests/test_near_ties.py tests/test_historical_source_binding.py
.venv/bin/python scripts/validate_results.py results/reference.json
# Run only after freezing the tested source; no concurrent benchmarks.
# 冻结被测源码后串行运行，不能与其他性能实验同时抢占资源。
PYTHONPATH=src .venv/bin/python benchmark.py --config configs/protocol-rowwise-20261013.json --output results/rowwise-20261013-local.json
.venv/bin/python scripts/validate_results.py results/rowwise-20261013-local.json
.venv/bin/python scripts/analyze.py results/rowwise-20261013-local.json --output-dir results/rowwise-20261013-analysis
```

Choose another fresh output path if one already exists. The benchmark refuses overwrites. Save the new result, source snapshot and generated analysis together. Do not overwrite `results/reference.json` or its analysis, pool old/new timings, or relabel old CI as verification of this repair. The frozen source must be unchanged during measurement. A failed run remains a failure record.

## Local acceptance after the repair

With the locked dependencies on Python 3.12.14, 93 tests passed; two timing-related tests (`test_benchmark_evidence_roundtrip`, `test_failure_preserves_completed_samples`) were not run to preserve serial measurement scheduling. Ruff format/lint, mypy, wheel/sdist build, 22-document bilingual/link/example checks, historical evidence binding and package exclusion checks passed locally. This supplements the 69-test focused numerical check; it does not add a performance run or remote CI evidence.
