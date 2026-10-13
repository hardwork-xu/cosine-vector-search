# 数值修复与尚未测量的性能边界

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

**状态：修复后内核性能尚未测量。** 新对照是采用同一逐行评分内核的穷举扫描，不是旧优化BLAS扫描。原1.50倍延迟目标及30%评分比例目标仅作为新运行的目标保留；正确性收紧为分数完全一致（`atol=rtol=0`）及有序ID一致。不预先宣称达标，也不建立相对原生 BLAS、Faiss 或真实嵌入检索的优势。独立计时的强原生/BLAS基线仍然缺失；本协议只比较内部数值一致的 B/C 路径。

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

Python 3.12.14 和锁定依赖下 93 项测试通过；两项含计时的测试（`test_benchmark_evidence_roundtrip`、`test_failure_preserves_completed_samples`）为保持串行测量安排而未运行。Ruff 格式/lint、mypy、wheel/sdist 构建、22 份文档双语/链接/示例检查、历史证据绑定及包排除检查均在本地通过。这补充了此前 69 项专项数值检查，不新增性能运行或远端 CI 证据。
