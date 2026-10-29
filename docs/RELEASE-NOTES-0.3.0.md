# v0.3.0 — Target-led design admission

## 中文

本轮将“方案值得面向用户目标立项”落实为候选训练前的必要条件。它在现有模块审查中完成，不新增常驻审稿流程。

- 目标适配：结合相关目标期刊/层次的论文原文，说明问题价值、贡献分量和可行证据范围；只有新意、公式差异或可运行性不足以放行。
- 数据针对性：把项目真实事实/限制与拟改变的机制串起来；仅复用当前数据、模型或发现辅助任务现象不足以建立必要性。
- 机制必要性与设计可靠性：核对最近邻、更简单方法、关键假设、信息流与反例；已知关键缺陷需有修复及复核证据。
- 新增 [设计立项规程](../skills/ai-research-workflow/references/admission.md) 和 [记录模板](../skills/ai-research-workflow/assets/admission.md)。四项核心依据充分才记录 `design_supported`，之后再评估 `proceed_to_pilot`；不足时返回 `needs_design_revision`。
- 带候选参数更新的 smoke、短训练及效果比较受同一准入；改称诊断或工程探针不豁免。立项前可做有明确问题与边界的事实、代数和只读诊断。
- 设计通过不提前证明涨点、稳定性或录用，更不认证绝对零缺陷；尚未测得效果也不自动否定依据充分的设计。

调用名、安装目录和 `research_guard.py` 及其 schema 保持兼容。登记工具不解析立项报告或自动判断论文质量；主执行者负责核对实际记录和阻断项。首次失败后最多两轮修复、全局预算和截止继续适用。

### 升级与旧项目

备份旧安装，再替换技能目录；下一次调用读取新版。现有项目沿用协议、账本、候选族、活动运行及已耗预算。旧“值得试”报告若缺关键立项依据，后续候选训练前补当前审查；不追认过去已合格，不重置历史，也不因技能升级自动停止、启动或重跑研究作业。新方法版本复核受影响条目，未改变且有效的证据可直接继承。

本轮实际验证范围见 [v0.3.0 验证记录](VALIDATION-0.3.0.md)。合成行为检查不证明真实研究创新、模型涨点或期刊录用。

## English

Candidate training now requires a reasoned design-admission decision tied to the user's publication/research target: target fit, dataset relevance, mechanism necessity and design reliability. The existing module review records evidence, critical defects, remaining assumptions and a version-bound decision. A formula difference or runnable method alone is insufficient.

`design_supported` precedes consideration of `proceed_to_pilot`. Missing measured effectiveness is not itself a design rejection; missing core rationale is not deferred to training. Optimizer-bearing smoke and short effect trials remain candidate training under any label. Bounded fact, algebra and read-only diagnostics can resolve specific design gaps.

The unchanged registry does not interpret admission reports or certify scientific quality. Existing contracts/history, the two-repair ceiling, budgets and deadlines remain intact. This preview improves the procedure; see [validation](VALIDATION-0.3.0.md) for actual tested scope and limitations.
