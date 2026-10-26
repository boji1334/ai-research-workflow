# Industrial Vision Research

面向 **Codex** 的工业视觉科研实验 skill，专注缺陷检测及相关的小样本、自监督研究。先了解项目和论文要求，再推进查新、创新模块设计、有限实验和两道审查，交付可复现的实验与贡献证据。

**当前版本：v0.1.0，早期版本。** 已完成的检查与待验证范围见 [验证记录](docs/VALIDATION.md)。真实工业视觉项目的端到端有效性仍待验收；创新性、实验提升与期刊录用均以实际证据判断。

## 工作方式

```text
阅读已有材料 → 项目事实访谈 → 论文目标与周期 → 冻结评价协议
    → 查新与机制设计 → 模块审查 → 有限小试
    → 公平对比、消融及必要实验 → 结果审查 → 实验证据交付
```

- **启动访谈是必要步骤。** 新项目不因引用 skill 就立即设计模块或训练。已有材料能回答的问题不重复问；项目事实澄清后再确认目标期刊/级别、OA 偏好与可接受周期。
- **追求可证实的创新和效果。** 检查最近邻原文、公式、监督与实现路径；提升标准结合任务、强基线、波动、工程价值及目标论文要求制定。
- **两道审查。** 模块审查检查创新与可实现性；结果审查核对原始产物、公平性、稳定性、消融解释和成本。审查意见必须定位证据、说明影响并给最小修复。
- **有限失败投入。** 新颖但首次无提升的候选，最多追加两轮有明确依据的小规模修复；仍无收益则关闭。已知但有提升的增强保留，并与原基线分别记录。
- **尊重周期与主线。** 预计超期时提前说明差距并询问取舍；没有调整就按原周期交阶段结果。关闭候选不等于放弃用户固定主线。
- **首版到实验结束。** 交付代码、配置、结果、权重位置、对比/消融、审查和复现入口，写论文留给后续请求。

## 安装

技能本体位于 [`skills/industrial-vision-research`](skills/industrial-vision-research)。核心是 Markdown 与模板，无需安装 Docker、AI Scientist v3 或上游科研套件。可选登记工具只需 Python 3.10+ 标准库。

[Releases](https://github.com/boji1334/industrial-vision-research/releases) 提供独立技能 ZIP 与 SHA-256 校验文件，解压后的 `industrial-vision-research/` 即为技能目录。

在 Codex 中调用已安装的官方 `skill-installer`：

```text
$skill-installer Install the skill from https://github.com/boji1334/industrial-vision-research/tree/main/skills/industrial-vision-research
```

也可以下载仓库，将该技能目录复制到研究项目的 `.agents/skills/industrial-vision-research`。例如在研究项目根目录使用 PowerShell（替换实际下载路径）：

```powershell
New-Item -ItemType Directory -Force -Path .agents/skills
Copy-Item -Recurse -LiteralPath "D:/downloads/industrial-vision-research/skills/industrial-vision-research" -Destination ".agents/skills/industrial-vision-research"
```

安装后重新打开或重启 Codex 会话，使其发现技能。目录规则与发现机制参见 [OpenAI 官方技能文档](https://developers.openai.com/codex/skills/)。若同名目录已存在，先比较版本再更新，避免覆盖自定义内容。

## 使用

```text
$industrial-vision-research 接手当前工业缺陷检测项目，先读已有材料并问清项目事实，再确认论文目标和周期。

$industrial-vision-research 继续当前研究，先核对最新协议、活动运行和候选审查，再推进下一步。

$industrial-vision-research 审查这个模块与最近邻工作的差异，以及已有实验是否支持机制解释，暂不训练。
```

第一次调用请提供项目材料或可访问的位置。实际训练需要用户已有或明确约定的环境、数据、执行权限、算力与存储预算。联网查新需要可用检索/浏览能力；缺少原文时保留待核结论。

代理分工使用当前环境中可用的 Codex 子代理能力，按关键审查阶段启用，无需混合多家 AI。若子代理不可用，如实标记单代理自审。技能本身不实现常驻调度器，也不会自动创建定时任务。

## 可选运行校验

[`research_guard.py`](skills/industrial-vision-research/scripts/research_guard.py) 可以检查协议字段、登记运行、抑制重复指纹、限制同一候选最多两次修复，并保留证据摘要。它不执行记录的命令，也不自动判定实验提升或原创性。

详细用法及边界见 [状态与交付](skills/industrial-vision-research/references/state-and-delivery.md)。已有运行管理工具时直接沿用，避免多份账本。

本地检查：

```text
python -m unittest discover -s tests -v
python tools/validate_repository.py
```

## 设计来源

借鉴 AI Scientist v3 的阶段接续与产物追踪、ARS 的问题澄清与来源核验、Orchestra 的研究构思与两层实验循环，以及 K-Dense 的证据审查思路。所有核心说明、领域规则、模板与辅助代码在本仓库重新编写；未打包这些上游项目或将其作为运行依赖。

固定到源码提交的来源、借鉴范围与冲突处理见 [来源说明](skills/industrial-vision-research/references/sources.md)。本项目独立维护，与上游团队无隶属关系。

贡献问题或建议可通过 GitHub Issues 提交；请提供脱敏后的最小例子。发布技能仓库不包含公开用户研究数据、权重或未发表创新的授权。

MIT License，见 [LICENSE](LICENSE)。
