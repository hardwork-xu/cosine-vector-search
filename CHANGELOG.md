# Changelog / 变更记录

## Unreleased — 2026-10-13

- Fix legal near-tie scan/block mode disagreements using one rowwise float64 candidate-scoring kernel. No rounding, clipping or relaxed tolerance.
- Add 20 adversarial/core regression cases; 69 focused tests passed locally. Integrated non-timing checks passed 93 tests, format/lint, typing, documentation and package builds; the two deferred timing tests subsequently passed (95 tests across two invocations).
- Retain the exact historically measured source and bind it only to the exact original raw record. Preserve historical 10.20× and adverse results as old-source measurements.
- Measure the corrected kernel with a separately frozen protocol: 8 workloads / 6,720 repeated timed calls; zero observed score error. The primary shared-kernel ratio is 10.83×; four slower-than-scan cases are retained. No native/BLAS comparison or new release is claimed.

- 统一逐行float64候选评分，修复合法近似并列输入的扫描/分块不一致，不取整、不裁剪、不放宽容差。
- 增加20项对抗/核心回归，本地专项69项通过；整合非计时检查 93 项通过，格式/lint、类型、文档和包构建通过；两项暂缓计时测试随后通过（全部 95 项分两次调用）。
- 准确存档历史被测源码，只接受与准确原始结果绑定的存档；保留10.20倍及不利结果为旧源码测量。
- 按独立冻结协议实测修复内核：8 工作负载/6,720 次重复计时调用，最大观察分数误差为零。主场景共享内核比值 10.83 倍，保留四个慢于扫描的场景；不声称原生/BLAS 对照或新 Release。
