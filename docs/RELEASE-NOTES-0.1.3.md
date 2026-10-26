# v0.1.3 — Isolated review and literature evidence

## 中文

将 Nature Skills 的部分审查与文献流程独立适配进视觉研究实验工作流，来源固定到已查阅提交，具体范围见[来源记录](../skills/ai-research-workflow/references/sources.md)。

- 正式模块和最终结果审查默认三份隔离上下文内部报告，使用同一冻结证据包和预先确定的阅读重点；小试与局部复核按风险和预算缩减并说明限制。
- 报告独立定稿后，单独复核算术、指标口径、图表/日志一致性和产物来源，再做综合；保留原报告，审计发现与审查者共识分列。
- 问题保留固定 ID、主张与证据位置、阻断范围、解决标准和复核证据。未解决阻断项不放行相应阶段；计划补实验本身不等于问题关闭。
- 新增多源查新与文献记录：版本关联去重、身份核验与命题支持分开，来源故障不冒充正常零结果，全文缺失保留机制待核。
- 首次失败后最多两轮小规模修复、候选族累计计数、总预算和截止日期继续适用。审查不产生额外实验额度。

调用名和安装目录保持 `ai-research-workflow`。辅助 Python 工具与协议/账本 schema 未改变，旧记录继续沿用；核心无需安装 Nature 套件、MCP 服务、Docker 或训练框架。上游的论文写作、投稿和 Nature 专属要求不在本次范围内。

本轮软件、打包与合成行为检查见 [v0.1.3 验证记录](VALIDATION-0.1.3.md)。内部隔离复核不等同外部同行评审，真实项目科研有效性仍待验收。

## English

This preview adapts selected Nature Skills review and literature-search methods to vision-model experiments, with pinned provenance. Formal module and final-result reviews default to three isolated internal reports over a frozen packet. Reports are finalized before a separate numerical/provenance audit and synthesis; scoped checks can reduce the count with documented limits.

Stable concern IDs link claims, evidence, blocking scope, resolution tests, and actual recheck evidence. Literature records separate source failures from empty results, reconcile paper versions, and distinguish citation identity from claim support. Neither review findings nor candidate renaming create extra repair rounds or extend the global budget/deadline.

The invocation, optional registry code, contract and history schemas remain unchanged. The skill needs no upstream suite, MCP service, Docker, or training framework installation. Manuscript/submission workflows and Nature-specific journal criteria are outside this change. See [this revision's validation record](VALIDATION-0.1.3.md) for tested scope and limitations.
