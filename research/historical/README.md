# Historical measured source / 历史被测源码

`20260921/index.py.source` is the exact former `src/capprune/index.py`, retained as
bytes rather than imported by the installed package. SHA-256:
`ab0afbaa8ee3d63efc43266b8bee249c00514a41ee8fe19f53088d3ebb850aad`.
It belongs to run `140ea5bb-9c95-4e8a-b2ab-17bcde0903ca` in
[reference.json](../../results/reference.json). This MIT project source retains
its original contents; all other measured core/harness/protocol/dependency files
must still match their recorded hashes. The validator permits this exact archive
only for the exact original result-file hash. It never accepts changed current
source as though it had been measured in the old run.

该文件逐字节保留历史被测实现，不由安装包导入。仅原始结果的完整文件哈希、
原路径、被测源码哈希均匹配时，验证器才接受此存档；其他核心、脚本、协议和
依赖文件仍须逐一满足记录哈希。新内核不能继承历史性能数字。
