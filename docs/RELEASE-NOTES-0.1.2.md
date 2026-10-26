# v0.1.2 — Review and experiment readiness

## 中文

本次为视觉模型科研技能的测试前修订，保留原研究目标与两轮小规模修复上限。

- 明确基线复核、小试结果审查、支持扩展后再补齐完整实验。
- 修复低分消融阻断后续实验的问题：以 `--kind control --reason "协议与对照目的"` 记录计划内消融和对照，仍计入总次数与资源预算。
- 完整方法确认失败仍阻止继续扩展；低分对照不会自动开启方法修复。
- 拒绝运行账本及其别名作为会在写入时改变的结果证据。
- 澄清仅审查的请求范围，完善视觉分类/分割评价和磁盘写入预算检查。
- 增加 9 项回归用例；附[审查记录](AUDIT-2026-10-26.zh-CN.md)与[项目试用清单](PILOT-TEST.zh-CN.md)。

安装目录与调用名沿用 `ai-research-workflow`。保留旧协议、账本和候选累计次数。旧记录仍可读取；使用新增 `control` 类型的账本需用 v0.1.2 或更新兼容版本，旧版工具不识别该类型。审查结论仍由执行者落实，CLI 不校验审查报告批准，也不测量实际算力/磁盘消耗。

## English

This preview fixes experiment bookkeeping and clarifies the baseline → pilot → result-review → expansion sequence, preserving the two-repair limit.

Planned comparisons and ablations use `--kind control` with a declared purpose. Controls count toward the global budget but do not substitute for full-method outcomes or unlock method repairs. Failed full-method confirmation still blocks expansion. The registry and its aliases are rejected as result evidence because finishing a run changes those files.

The update also clarifies review-only scope, vision-task metrics, and storage estimates, with nine added unit/CLI regressions and a project-pilot checklist. Existing records remain readable; registries containing the new control kind require v0.1.2 or a compatible later helper. Review approval and actual resource use remain procedural and project-tool responsibilities. Real-project scientific effectiveness is not established by software tests.
