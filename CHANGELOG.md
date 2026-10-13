# Changelog / 变更记录

## Unreleased — 2026-10-13

- Fix legal near-tie scan/block mode disagreements using one rowwise float64 candidate-scoring kernel. No rounding, clipping or relaxed tolerance.
- Add 20 adversarial/core regression cases; 69 focused tests passed locally. Integrated non-timing checks passed 93 tests, format/lint, typing, documentation and package builds; two timing tests remain unrun.
- Retain the exact historically measured source and bind it only to the exact original raw record. Preserve historical 10.20× and adverse results as old-source measurements.
- Add a separately named protocol for the changed kernel; new performance is not yet measured. No new release is claimed.

- 统一逐行float64候选评分，修复合法近似并列输入的扫描/分块不一致，不取整、不裁剪、不放宽容差。
- 增加20项对抗/核心回归，本地专项69项通过；整合非计时检查 93 项通过，格式/lint、类型、文档和包构建通过；两项计时测试未运行。
- 准确存档历史被测源码，只接受与准确原始结果绑定的存档；保留10.20倍及不利结果为旧源码测量。
- 为变更内核添加独立命名协议，新性能尚未测量；未声明新Release。
