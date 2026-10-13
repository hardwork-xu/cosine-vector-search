# 数值修复与实测性能边界

[English](../en/NUMERICAL_REPAIR.md) · [实验](EXPERIMENTS.md)

## 2026-10-13实际修复

合法的101×16近似重复向量（seed4、扰动1e-15、k10）在NumPy2.2.6下产生扫描与分块ID不一致。关闭剪枝的分块路径也不同，问题定位为候选分数的归约顺序，而非剪枝上界。这是实际模式一致性缺陷，不是否定实数算术下的球冠定理。

两条候选评分路径现统一调用 `_score_rows`，使用 `np.einsum("ij,j->i", vectors, query, optimize=False)`。没有裁剪、取整分数或放宽容差。建库聚类及保守球冠上界保持旧实现。本次已检查的NumPy2.2.6环境中，核心加20项新增回归共69项测试通过，覆盖五种维度/三种k的近似并列、完全重复、原始ID并列顺序、持久化及独立Python排序。测试不证明所有平台可靠，也不建立性能结论。

## 准确源码身份

- 历史数值源码：`ab0afbaa8ee3d63efc43266b8bee249c00514a41ee8fe19f53088d3ebb850aad`。准确字节保存在 [index.py.source](../../research/historical/20260921/index.py.source)，不在可导入包内。
- 本次修复后的数值源码：`28f7273416fd1d20c8062c2884167c2c0f39739f04e3fe2ee7a11b08940d7360`。
- 新协议：[protocol-rowwise-20261013.json](../../configs/protocol-rowwise-20261013.json)，SHA-256 `05d85870354eb512e67099e374f26e5eba8bb00f0d5187ad429e37a2a50af295`。
- 原始run `140ea5bb-9c95-4e8a-b2ab-17bcde0903ca`与[旧协议](../../configs/protocol.json)保持原样。10.20倍主要结果及全部历史负面结果仅属于旧源码。

验证器只在**完整原始结果文件哈希**、原源码路径和被测源码哈希全部匹配已登记历史记录时接受存档。其他运行时、基准、协议和依赖文件仍须逐一匹配记录哈希。修改或重新序列化旧结果不能套用该例外；新运行须绑定当前源码。历史归档校验通过不表示新代码已被历史实验测量。

## 新测量不能继承旧加速数字

**状态：修复内核已于 2026-10-13 按独立冻结协议完成实测。** 新对照是采用同一逐行评分内核的穷举扫描，不是旧优化BLAS扫描。1.50 倍延迟及 30% 评分比例目标在新运行前冻结，均在指定合成主场景通过；正确性收紧为分数完全一致（`atol=rtol=0`）及有序ID一致。这不建立相对原生 BLAS、Faiss 或真实嵌入检索的优势。独立计时的强原生/BLAS基线仍然缺失；本协议只比较内部数值一致的 B/C 路径。

原七个工作负载、顺序和种子全部保留，末尾追加500×64聚类场景。三种聚类规模为500/5,000/50,000，d64、k10；种子及簇数不同，属于覆盖测试而非控制变量的扩展规律。50,000×128及k100另覆盖维度/输出压力；各向同性50,000×64、真实digits和tiny k=N保留为不利/边界场景。各场景40条查询、7轮重复、4条预热、3种模式，8场景共6,720次计时。串行测量，保持源码、输入和请求单线程环境一致。下载/准备/建库不计入查询时间；建库/保存/加载另有记录。

digits来自scikit-learn1.7.2自带的 `load_digits`，1,797张图像各含64个原始像素特征；有种子排列划分40条查询和1,757条库向量。安装依赖后不需模型或数据网络下载。它是数值相似检索，不是语义嵌入或分类质量基线。保留[数据与依赖归属](../../NOTICE_zh.md)。

## 复现命令

使用uv0.8.22和已有锁文件。测量导入NumPy2.2.6、threadpoolctl3.6.0、psutil7.1.0、scikit-learn1.7.2（间接依赖SciPy）；分析使用Matplotlib3.10.6与pyparsing3.2.3。`uv sync --frozen`安装这些开发工具及锁定依赖，不通过改锁文件省略依赖。全局 uv 版本不匹配时使用 `uvx --from uv==0.8.22 uv sync --frozen`，无需修改全局可执行文件。`PYTHONPATH=src`保证测量当前工作树，而非别处旧的editable安装。

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

若输出路径已存在，另选新名称；脚本拒绝覆盖。保留新结果、源码快照及对应分析；不要覆盖 `results/reference.json`或旧图表，不合并新旧计时，不把旧CI当作本次修复验证。测量期间冻结源码，失败运行保留失败状态。

## 修复后的本地验收

Python 3.12.14 和锁定依赖下 93 项测试通过；两项含计时的测试（`test_benchmark_evidence_roundtrip`、`test_failure_preserves_completed_samples`）此前因串行测量安排暂缓，正式运行结束后单独执行，两项均通过（2.79 秒）。Ruff 格式/lint、mypy、wheel/sdist 构建、22 份文档双语/链接/示例检查、历史证据绑定及包排除检查均在本地通过。因此同一未变源码的全部 95 项测试分两次调用通过，补充此前 69 项专项数值检查；测试不能替代独立正式性能运行，也不证明远端 CI 状态。

## 10 月 13 日运行记录

唯一一次正式运行 `8e769ab6-6fed-4176-925f-8e49e855e75a` 开始于 `2026-10-13T04:07:00.492074+00:00`，结束于 `2026-10-13T04:07:11.638118+00:00`。[原始记录](../../results/rowwise-20261013.json) 对应源码提交 `9524ad45d6a8039e814af9671a34c25d573960dd`、聚合源码 SHA-256 `cbef37f7e457504bcdc6791282ea27dcd5ea316a9c5d522d1864b6ba7202b659`，原始文件 SHA-256 为 `c1763089bc31988c0f1bac40e49d4a34e18729ab614904d36415041251d54680`。全部登记源码文件哈希匹配，原七场景输入哈希及种子均保持一致。这证明来源绑定与输入复用，不证明旧新评分内核等价。

环境：Apple M1 Pro、arm64 Darwin 25.6.0、Python 3.12.14、NumPy 2.2.6 / Accelerate、SciPy 1.18.1、scikit-learn 1.7.2、threadpoolctl 3.6.0、psutil 7.1.0。NumPy 导入前请求单线程；Accelerate 内部实际线程数无法直接内省。没有同时运行其他性能实验。

统计单位为 **8 个工作负载，每个一个种子及 40 个查询索引**。每个场景复用查询集合进行 7 轮、3 模式计时，每场景/模式 280 次，总计 6,720 次调用；它们不是独立数据集，也不是 6,720 个独立观测。本次仅一个主机、一次完整运行。全部 ID 一致，零容差下最大观察分数误差为 **0**，八场景均通过正确性检查。

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

完整表由未变更的 `scripts/analyze.py` 从原始文件生成，见[生成中文表](../../results/rowwise-20261013-analysis/table_zh.md)、[统计](../../results/rowwise-20261013-analysis/summary.json)和[图](../../results/rowwise-20261013-analysis/benchmark.png)。统计保留四分位数及七个逐轮中位数；它们是描述性分布，不是置信区间。未剔除重复轮次或不利场景。

指定主场景满足预设目标：**10.83 倍 ≥1.50 倍**，评分 **2.34265% ≤30%**。中位查询延迟为扫描 1.1019585 ms、分块 1.6649165 ms、剪枝 0.1017500 ms。扫描和剪枝共享逐行内核，**这不是相对原生 BLAS 或 Faiss 的加速**。单独分块更慢，支持当前实现内避免评分/合并的有限收益；消融还改变遍历顺序，未隔离该交互。

四个场景慢于扫描：各向同性（耗时 1.46 倍）、真实 digits（4.66 倍）、tiny k=N（3.94 倍）及 500 行聚类（1.20 倍）。最后一个仅评分 8.265% 向量，仍因开销而更慢；结果否定普遍加速。跨规模种子及簇数不同，属于覆盖而非控制变量的扩展规律。没有证明语义质量、学习型嵌入、多种子稳健性、多主机推广或成熟研究成果。优化原生基线仍是关键未测对照。

查询计时包括校验、归一化、上界、评分、选择/合并及分配，不含生成数据、建库和持久化。主场景另记建库 163.951542 ms、保存 770.100000 ms、加载 89.076500 ms，各仅一次。`first_query_ns` 在正确性和 I/O 准备之后，不是冷启动。保留索引数组 52,033,272 字节，包含原始及打包布局；原始记录中的进程 RSS/高水位不是每模式内存。从中位数估算完整建库需 164 次查询摊销，不是实际应用盈亏点。旧 10.20 倍与新 10.83 倍不能合并或用于宣称修复加速。
