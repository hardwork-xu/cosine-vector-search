"""Regression for layout-dependent BLAS near ties / 布局相关近似并列回归。"""

from pathlib import Path

import numpy as np
import pytest

from capprune import CapIndex


@pytest.mark.parametrize("dimension", [3, 7, 16, 33, 64])
@pytest.mark.parametrize("k", [1, 10, 101])
def test_near_ties_have_identical_computed_scores_and_ids(dimension: int, k: int) -> None:
    # Seed 4, d=16, k=10 failed with NumPy 2.2.6 before the shared scoring kernel.
    # 修改前 NumPy 2.2.6 的 seed=4、d=16、k=10 曾产生不同结果。
    rng = np.random.default_rng(4)
    centers = rng.normal(size=(3, dimension))
    vectors = centers[np.arange(101) % 3] + rng.normal(size=(101, dimension)) * 1e-15
    queries = centers[:2].copy()
    index = CapIndex.build(vectors, n_clusters=7, iterations=3, seed=4)
    baseline = index.search(queries, k, mode="scan")
    for mode in ("blocked", "pruned"):
        actual = index.search(queries, k, mode=mode)
        np.testing.assert_array_equal(actual.ids, baseline.ids)
        np.testing.assert_array_equal(actual.scores, baseline.scores)


@pytest.mark.parametrize("dimension", [1, 7, 16, 65])
def test_duplicates_keep_original_id_ties_across_modes(dimension: int) -> None:
    # Exact duplicated rows require identical computed scores, not epsilon ties.
    # 相同向量的分数必须完全一致，不能靠误差阈值宣布并列。
    rng = np.random.default_rng(73)
    positive = rng.normal(size=dimension)
    vectors = np.array([positive if i % 2 == 0 else -positive for i in range(101)])
    index = CapIndex.build(vectors, n_clusters=9, iterations=3, seed=4)
    for mode in ("scan", "blocked", "pruned"):
        actual = index.search([positive, -positive], 10, mode=mode)
        np.testing.assert_array_equal(actual.ids[0], np.arange(0, 20, 2))
        np.testing.assert_array_equal(actual.ids[1], np.arange(1, 21, 2))
        for row in actual.scores:
            np.testing.assert_array_equal(row, np.repeat(row[0], 10))


def test_near_tie_scores_sort_without_clipping_and_survive_persistence(tmp_path: Path) -> None:
    rng = np.random.default_rng(4)
    centers = rng.normal(size=(3, 16))
    vectors = centers[np.arange(101) % 3] + rng.normal(size=(101, 16)) * 1e-15
    index = CapIndex.build(vectors, n_clusters=7, iterations=3, seed=4)
    queries = centers[:2]
    # Obtain every actual score, then use a separate Python ordering oracle.
    # 获取所有实际分数，再用独立 Python 排序核对分界并列；不复制 top-k 算法。
    full = index.search(queries, 101, mode="scan")
    expected = []
    for ids, scores in zip(full.ids, full.scores, strict=True):
        ordered = sorted(
            zip(ids.tolist(), scores.tolist(), strict=True), key=lambda pair: (-pair[1], pair[0])
        )
        expected.append([pair[0] for pair in ordered[:10]])
    path = tmp_path / "near-ties.npz"
    index.save(path)
    for candidate in (index, CapIndex.load(path)):
        for mode in ("scan", "blocked", "pruned"):
            result = candidate.search(queries, 10, mode=mode)
            np.testing.assert_array_equal(result.ids, expected)
            np.testing.assert_array_equal(result.scores, full.scores[:, :10])
