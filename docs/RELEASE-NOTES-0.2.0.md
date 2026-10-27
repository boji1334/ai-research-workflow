# v0.2.0 — Research positioning and experimental decisions

## 中文

本轮加强从前沿查新到实际小试的决策，减少连续提出已知机制、扩大审查却迟迟没有新候选的循环。

- 新增 [研究定位与机会选择](../skills/ai-research-workflow/references/positioning.md) 与可选 [机会模板](../skills/ai-research-workflow/assets/opportunity.md)：区分方向、问题、机制和证据，从最近邻实际范围与项目限制选择可实验的机会。
- 区分用户硬约束与技术偏好；场景、数据角色或论文目标的实质变化先解决需求，不自行切换任务。
- 小试准入、扩大实验和最终贡献验收分别判断。成熟组件不自动否定整体机制；未知效力由实验回答，明确错误和已证实重复按具体影响处理。
- 预先记录正向、无差异、下游无收益和工程失败的解释，围绕相关有效强基线设计最小区分实验。
- 对定位、查新、审查和工程恢复设置项目适用的累计边界，分开记录已用、预留和可用资源。保留首次失败后最多两轮小修、候选族历史、全局预算和截止。
- 阶段汇报分别列出模型新增、证据新增和工程恢复；继承的模型与成绩保留原版本归属。

调用名仍为 `ai-research-workflow`。`research_guard.py`、合同和登记 schema 未改变；新增记录是项目规程，不是 CLI 自动判新颖性、授权审查或新增调度能力。无需安装上游套件、Docker 或训练依赖。

### 升级与在途实验

备份已有安装并保留本地修改，再替换技能目录。下一次调用读取新版规程。已有项目沿用协议、账本、活动运行与累计修复次数；先恢复现场和责任，不因升级重训、重评或重新初始化登记文件。定位/预算调整按原协议的版本和摘要规则留痕，已经冻结的实验继续按其实际协议解释。

行为检查和软件验证的实际范围见 [v0.2.0 验证记录](VALIDATION-0.2.0.md)。本轮未将真实科研项目材料纳入发布包；合成检查通过不证明能够产生原创模块、提升真实模型或达到某一期刊水平。

## English

This preview strengthens the decision between literature review and a bounded experiment. Research positioning connects the nearest methods' actual scope, a project-grounded limitation, a distinct mechanism hypothesis and a discriminating test. Prior work in a direction and familiar components are evaluated at their proper scope; missing experiments do not establish a research gap.

Pilot admission, experimental expansion and contribution acceptance are separate decisions. Findings identify the affected action or claim. Outcome branches are recorded before a pilot, relevant effective baselines are retained, and positioning/review/engineering time is bounded alongside training. Reports distinguish inherited scores, model changes, additional evidence and recovery work.

The invocation, optional Python registry and schemas remain compatible. Existing protocols, reservations, candidate histories and repair counts must be preserved during migration. The procedure does not automatically enforce scientific judgments, launch scheduling or increase budgets. See [validation and limitations](VALIDATION-0.2.0.md).
