# v0.1.1 — AI Research Workflow

## 中文

项目由 **Industrial Vision Research** 更名为 **AI Research Workflow**，定位调整为倾向计算机视觉与视觉模型研究。工业视觉与缺陷检测保留为应用场景之一。

本次更新保留原有项目访谈、查新、模块审查、结果审查、实验验收和止损规则：首次无提升后最多追加两轮有依据的小规模修复；关闭候选后，在剩余周期与预算内寻找不同机制。运行工具、协议格式和修复计数逻辑沿用 v0.1.0。

### 安装与迁移

新技能目录为 `skills/ai-research-workflow`，调用名为 `$ai-research-workflow`。独立 ZIP 解压后顶层为 `ai-research-workflow/`，可放入研究项目的 `.agents/skills/`。

已有安装时，先比较和保留旧目录中的个人修改，再用新目录替换旧技能入口，避免同时启用两份。研究项目中的协议、候选账本、运行记录、数据和权重保留原位；更名不重置实验历史或预算。更新后启动新的 Codex 会话。

旧版本 v0.1.0 的标签和压缩包保持原样。软件检查与历史行为检查的范围见[验证记录](VALIDATION.zh-CN.md)。真实视觉研究项目的端到端验收仍待完成。

## English

**Industrial Vision Research** is renamed to **AI Research Workflow**, with an emphasis on computer vision and vision model research. Industrial vision and defect detection remain application examples.

The established intake, novelty checks, module/result reviews, acceptance criteria, and stopping rules are preserved. The helper, contract format, and repair accounting are unchanged from v0.1.0. This release updates identity, scope wording, links, and installation paths.

Install `skills/ai-research-workflow`, or extract the standalone ZIP's `ai-research-workflow/` directory into the project's `.agents/skills/`. Invoke it with `$ai-research-workflow`. Compare and preserve local customizations before replacing an old installation, keep one active copy, and start a new Codex session. Existing research ledgers, contracts, datasets, and artifacts stay in place; migration does not reset history or budgets.

The original v0.1.0 tag and assets are retained. See the [validation record](VALIDATION.md) for the software checks and the provenance of historical behavior checks. Real-project research effectiveness remains to be evaluated.
