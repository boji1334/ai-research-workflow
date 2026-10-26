# 设计来源与适配边界

本仓库独立编写规程、领域规则、模板和 Python 辅助代码，未分发上游源码或整段提示词，也未将上游包作为运行依赖。下面是查阅来源与设计借鉴的记录，不表示上游为本项目背书，或所有原有能力已移植。

查阅日期：2026-10-26。链接固定到本次核对的提交；后续上游更新不会自动改变本技能行为。

## AI Scientist v3 — 阶段接续与产物追踪

- 来源：[SakanaAI/AI-Scientist-v3 pipeline.md](https://github.com/SakanaAI/AI-Scientist-v3/blob/df8313889a004f8a44a472e19a833cd547bb828a/docs/pipeline.md)。
- 借鉴：研究探索、消融、最终评价、事后分析等阶段的接续，以及统一运行标识和可恢复的产物路径。
- 适配：项目与论文需求由访谈澄清；首版止于实验；阶段结束以用户目标和原始证据判断。
- 边界：没有集成 `agsci`、容器、API 服务或其代理运行器。上游可选最终稿 `review` 是非阻断步骤，不能直接替代这里的模块/结果两道审查。

## ARS-Codex — 问题澄清与来源核验

- 来源：[academic-research-suite/SKILL.md](https://github.com/Imbad0202/academic-research-skills-codex/blob/c923a914eaa45fe1435ad3ac6641a8f251167675/skills/academic-research-suite/SKILL.md)。
- 借鉴：研究问题未明确时先澄清、按阶段读取必要材料、文献与研究材料的可追溯性。
- 适配：面向视觉模型研究明确数据角色、学习协议、基线、历史尝试、资源、论文目标和周期。
- 边界：未复制其总路由、工作流或 agent 提示词。文献身份核验与命题支持、新颖性证明分别处理。其医学/临床特定分级不套用于机器学习实验。

## Orchestra Research — 构思与内外两层循环

- 来源：[brainstorming-research-ideas](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/21-research-ideation/brainstorming-research-ideas/SKILL.md)、[autoresearch](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/0-autoresearch-skill/SKILL.md)。
- 借鉴：从真实问题/失败边界寻找机制假设；快速实验与整体研究方向判断分开；实验前确定协议；记录负结果。
- 适配：补充张量、梯度、监督和实现路径，候选首次无提升后最多追加两轮有限修复。
- 边界：不继承其优先创建持续循环、持续推进到底或自动进入论文写作的默认要求；不把固定研究主线随意更换。未打包其其他领域技能。

## K-Dense — 证据与解释审查

- 来源：[scientific-critical-thinking](https://github.com/K-Dense-AI/scientific-agent-skills/blob/593377bb048752abb0152deab9fbb1083a6087df/skills/scientific-critical-thinking/SKILL.md)。
- 借鉴：明确实验单位；先提取证据再评价；检查混杂、依赖、统计解释；将结论与可定位的证据对应，并给可行修复。
- 适配：原始预测/日志复算、公平训练和调参预算、小样本支持集、预训练数据接触、弱类、消融解释与计算成本。
- 边界：未移植临床 GRADE/Cochrane 等特定评估工具，未集成其可选绘图或第三方付费 API。

## Nature Skills — 隔离审查、数值核验与文献证据

- 来源：固定提交 `07009f91f99c7108519e7657885f1a89d91099d5` 的 [nature-reviewer](https://github.com/Yuan1z0825/nature-skills/blob/07009f91f99c7108519e7657885f1a89d91099d5/skills/nature-reviewer/SKILL.md)、[审查执行流程](https://github.com/Yuan1z0825/nature-skills/blob/07009f91f99c7108519e7657885f1a89d91099d5/skills/nature-reviewer/references/reviewer-workflow.md)、[数值与一致性审计](https://github.com/Yuan1z0825/nature-skills/blob/07009f91f99c7108519e7657885f1a89d91099d5/skills/nature-reviewer/references/forensic-consistency-audit.md)，以及 [nature-academic-search](https://github.com/Yuan1z0825/nature-skills/blob/07009f91f99c7108519e7657885f1a89d91099d5/skills/nature-academic-search/SKILL.md) 的[多源检索](https://github.com/Yuan1z0825/nature-skills/blob/07009f91f99c7108519e7657885f1a89d91099d5/skills/nature-academic-search/references/workflows/wf1-multi-source-search.md)与[引用核验](https://github.com/Yuan1z0825/nature-skills/blob/07009f91f99c7108519e7657885f1a89d91099d5/skills/nature-academic-search/references/workflows/wf2-citation-verification.md)流程。
- 借鉴：相同冻结证据包、预先指定阅读重点、隔离报告定稿后综合；单独进行数值/来源核验；问题 ID、阻断范围、解决标准与证据追踪；多源查询、版本去重、身份与命题支持分开核实、单源故障时保留覆盖缺口。
- 适配：独立编写为视觉研究实验规程；正式模块/最终结果审查默认三份隔离内部报告，小试和局部复核按实际风险与预算缩减并注明。审查发现进入已有候选族、两轮修复和全局预算，不新增无限实验循环。记录模板和范围见 [审查流程](review.md) 与 [文献流程](literature.md)。
- 边界：未移植其提示词、脚本、MCP 服务、安装器或完整科研套件。目标按用户期刊和任务设定；未默认采用 Nature 投稿结构、特定审稿轴或医学渠道。模型内部隔离审查不表述为外部同行评审，审计发现不冒充审查者共识。
- 上游许可：本次核对的 [LICENSE](https://github.com/Yuan1z0825/nature-skills/blob/07009f91f99c7108519e7657885f1a89d91099d5/LICENSE) 为 Apache-2.0；这里记录流程设计来源，未再分发上游文件。安装或再分发上游时遵循其对应通知与许可。

## Codex 技能格式

- 来源：[OpenAI 官方 agent skills 文档](https://developers.openai.com/codex/skills/)。
- 使用：`SKILL.md` 的名称与描述、渐进读取支持文件、`.agents/skills` 发现方式及可选界面元数据。
- 技能规程由 Codex 与可用工具执行；技能文件本身不提供后台服务或训练运行时。

本仓库的 MIT 协议适用于本仓库原创内容。独立安装或再分发上游项目时，按对应上游当时的许可证与通知要求处理。
