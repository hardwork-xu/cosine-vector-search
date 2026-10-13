# Numerical repair and measured performance boundary

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

**Status: the corrected kernel was measured on 2026-10-13 under the separate frozen protocol.** The new comparator is exhaustive scoring through the same rowwise kernel; it is not the former optimized BLAS scan. The 1.50× timing target and 30% scoring target were frozen before the new run; both passed for the named synthetic primary case. Correctness is tightened to identical scores (`atol=rtol=0`) and ordered IDs. This does not establish superiority to native BLAS, Faiss or real embedding retrieval. A separately timed strong native/BLAS baseline is still missing; this protocol compares internally consistent B/C paths only.

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

With the locked dependencies on Python 3.12.14, 93 tests passed; two timing-related tests (`test_benchmark_evidence_roundtrip`, `test_failure_preserves_completed_samples`) were initially deferred to preserve serial measurement scheduling, then passed together in a separate 2-test invocation (2.79 seconds) after the official run. Ruff format/lint, mypy, wheel/sdist build, 22-document bilingual/link/example checks, historical evidence binding and package exclusion checks passed locally. Thus all 95 tests passed across the two invocations on unchanged source. This supplements the 69-test focused numerical check; these tests do not replace the separate official performance run or establish remote CI status.

## Recorded October 13 result

The single official run `8e769ab6-6fed-4176-925f-8e49e855e75a` started at `2026-10-13T04:07:00.492074+00:00` and finished at `2026-10-13T04:07:11.638118+00:00`. Its [raw record](../../results/rowwise-20261013.json) identifies source revision `9524ad45d6a8039e814af9671a34c25d573960dd`, aggregate source SHA-256 `cbef37f7e457504bcdc6791282ea27dcd5ea316a9c5d522d1864b6ba7202b659`, and raw-file SHA-256 `c1763089bc31988c0f1bac40e49d4a34e18729ab614904d36415041251d54680`. All registered source-file hashes match; all seven original input hashes and seeds remain identical. This verifies provenance and input reuse, not equivalence of historical/current scoring kernels.

Environment: Apple M1 Pro, arm64 Darwin 25.6.0, Python 3.12.14, NumPy 2.2.6 / Accelerate, SciPy 1.18.1, scikit-learn 1.7.2, threadpoolctl 3.6.0 and psutil 7.1.0. One thread was requested before NumPy import; Accelerate's effective internal thread count is not directly introspectable. No other performance experiment ran concurrently.

The statistical units are **8 workload cases with one seed each and 40 query indices per case**. Each case reuses its query set over 7 repetitions and 3 modes, giving 280 timings per mode/case and 6,720 timed calls overall; these are not independent datasets or 6,720 independent observations. This is one host and one complete run. All IDs agreed and maximum observed score error was **0**, with zero tolerance; all eight cases passed correctness.

| Case / 场景 | Scan ms | Blocked ms | Pruned ms | Speedup / 加速比 | Scored / 评分比例 | Build ms |
|---|---:|---:|---:|---:|---:|---:|
| clustered_n5000_d64 | 0.1298 | 0.3631 | 0.0475 | 2.73× | 4.9% | 20.5 |
| clustered_n50000_d64 | 1.1020 | 1.6649 | 0.1018 | 10.83× | 2.3% | 164.0 |
| clustered_n50000_d128 | 2.1848 | 2.6279 | 0.1469 | 14.88× | 3.1% | 301.1 |
| isotropic_n50000_d64 | 1.1599 | 1.6343 | 1.6891 | 0.69× | 100.0% | 165.0 |
| clustered_n50000_k100 | 1.1322 | 1.8732 | 0.1135 | 9.97× | 2.8% | 158.5 |
| digits_real | 0.0582 | 0.2958 | 0.2711 | 0.21× | 84.4% | 6.5 |
| tiny_k_equals_n | 0.0175 | 0.0561 | 0.0689 | 0.25× | 100.0% | 1.6 |
| clustered_n500_d64 | 0.0316 | 0.1429 | 0.0378 | 0.84× | 8.3% | 2.2 |

This full table is generated from the raw file by unchanged `scripts/analyze.py`; see [generated English table](../../results/rowwise-20261013-analysis/table_en.md), [summary](../../results/rowwise-20261013-analysis/summary.json) and [plot](../../results/rowwise-20261013-analysis/benchmark.png). Quartiles and seven per-repeat medians remain in the summary; they are descriptive distributions, not confidence intervals. No repetitions or unfavorable cases were dropped.

The primary case met its premeasurement targets: **10.83× ≥1.50×**, scoring **2.34265% ≤30%**. Median query times were 1.1019585 ms scan, 1.6649165 ms blocked and 0.1017500 ms pruned. Scan and pruning both use the shared rowwise kernel: **this is not a speedup over native BLAS or Faiss**. Block traversal alone was slower, supporting a narrow within-implementation benefit from avoiding scores/merges. The ablation also changes traversal order and does not isolate that interaction.

Four cases lost to scan: isotropic (1.46× longer), real digits (4.66×), tiny k=N (3.94×) and 500-row clustered data (1.20×). The last scored only 8.265% of vectors but still lost due to overhead. These results reject universal acceleration. Cross-size cases have different seeds/cluster counts, so this is workload coverage, not a controlled scaling law. No semantic quality, learned embeddings, multi-seed robustness, multi-host generalization or mature research status is established. An optimized/native baseline remains an essential unmeasured comparator.

Query timers include validation, normalization, bounds, scoring, selection/merging and allocation; they exclude data generation, build and persistence. The primary case separately recorded 163.951542 ms build, 770.100000 ms save and 89.076500 ms load, each once. `first_query_ns` follows correctness and I/O preparation and is not cold startup. Retained index arrays were 52,033,272 bytes, including both original and packed layouts; process RSS/high-water values in the raw file are not per-mode memory. Estimated full-build amortization is 164 queries from medians, not an observed application break-even. The old 10.20× and new 10.83× ratios must not be pooled or used to claim a repair-induced speed increase.
