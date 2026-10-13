Measured results; requested one CPU thread, float64, online batch=1. Medians include all repeats; no tail-latency claim.

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
