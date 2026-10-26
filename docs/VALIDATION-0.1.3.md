# v0.1.3 validation / 验证记录

Date / 日期：2026-10-26。

This revision changes skill instructions, references, templates, and documentation. The optional Python registry code and its schema are unchanged. Validation results are recorded below before publication. Real vision research effectiveness remains an outstanding project test.

本轮为规程和模板更新，实验登记工具与 schema 未改变。软件检查、隔离内部行为检查与真实科研验收分别记录。

## Software and package / 软件与打包

- 40 standard-library unit/CLI tests passed locally on Windows, with no skips. The registry implementation is unchanged.
- Official skill static validation passed (`Skill is valid!`); repository relative links, Python/JSON parsing, UI YAML and version metadata passed. `git diff --check` passed.
- The release-content scan found no local user paths, private-key markers, or the credential patterns inspected in the publication files. The manifest contains only skill/documentation/software-test material.
- The standalone ZIP is checked for integrity, exact extraction agreement and a relocated CLI check; its `SHA256SUMS` accompanies the release.
- The existing Windows/Linux × Python 3.10/3.12 CI matrix applies to this revision. See the actual commit runs in GitHub Actions; local behavior checks are distinct from CI.

## Three isolated reports / 三份隔离报告

The primary executor supplied the same immutable synthetic packet from `tests/fixtures/result-review/` to three Codex subagents with `fork_context=false`. Emphases were fixed before dispatch: novelty/theory, implementation/experimental validity, and stability/generalization/cost. Each received the same skill rules and report template, with no expected verdict, suspected issue list, prior report, or historical validation answer. Each was instructed to read only that packet and the necessary skill files, run short local calculations if useful, and save a separate report. No reviewer received another report or shared ledger.

All three reports were completed before the primary executor read them, ran the post-review audit and wrote this synthesis. Their byte hashes were recorded and the reports were retained unchanged. Isolation was enforced by separate conversation contexts and the scoped tasks, not filesystem access controls; the filesystem itself was shared.

| Finding independently raised | Report issue IDs |
|---|---|
| All planned seeds give a negative mean delta; a best-run +2 does not establish stable gain | R1-01; R2-01; R3-001 and R3-002 |
| Added synthetic data and doubled optimizer updates violate the recorded fair-comparison condition | R1-02; R2-02; R3-003 |
| Gate causality lacks a discriminating ablation | R1-04; R2-03; R3-004 |
| Novelty/nearest-neighbor and module-review evidence is absent from the packet | R1-03; R2-06; R3-005 |
| Prediction-level evaluation and experiment provenance remain unverified | R1-05; R2-04 and R2-05; R3-006 |

Each report chose `unsupported_or_negative`, retained the failed seed, separated a stage report from research success, provided claim/evidence pointers, blocking scope and resolution tests, and kept substantive issues open without closure evidence. No report claimed to have recomputed prediction-level AP, proved leakage/fabrication, verified novelty, or authorized new training. Differences in grouping and emphasis were preserved. Agreement is an observation of these reports, not independent scientific evidence.

Frozen report SHA-256 values:

```text
R1 91b2794d6f4ec6172fbc743dfafcf0b7ad2f18a995bef0297a72f56bb91645ab
R2 96ae64a06edc083584acc4441057acc7cc4a3422d19a3a4a1682b7a2781a73fd
R3 644296c8b2e563232eab354ddb633aaf78457bf12ac97e7c63d65a1e69cd996e
```

Raw reports remain local because their execution provenance includes local paths; the public record publishes hashes and this bounded summary, not rewritten reviewer reports.

## Post-review audit / 定稿后独立核验

After all reports were finalized, the primary executor separately parsed the CSV and protocol using Python's standard library and verified that the packet hashes were unchanged.

| Audit item | Actual result and limit |
|---|---|
| Planned seed coverage and unique method/seed rows | Passed for all six supplied rows. |
| AP range | All supplied scores lie within the stated 0–100 scale. This does not verify their measurement. |
| Full-seed means | Baseline 80.000000; candidate 74.333333; delta −5.666667 AP points. The +2.0-point mean-gain requirement is not met. |
| Per-seed deltas | +2, −21, +2. The displayed 80→82 arithmetic is correct for one run. |
| Sample standard deviations (n−1) | Baseline 1.000000; candidate 12.423097; paired delta 13.279056. Descriptive values, not a significance test. |
| Fairness fields | Training-data labels differ, and recorded updates are 1000 vs 2000. Confirmed protocol mismatch; no measured wall-time ratio inferred. |
| AP reconstruction and test independence | Not assessable from supplied inputs; predictions, labels, evaluator and provenance are absent. |
| Anomaly interpretation | Wide dispersion was recorded; no data-integrity violation was inferred. |

The audit independently corroborated arithmetic and field-level findings. It found no additional confirmed issue in its bounded scope. Audit results were not fed back to reviewers, and no report was edited. Consensus above is based on the independently frozen report IDs, separately from this audit.

## Continuation and literature / 接续与文献行为

A fourth isolated Codex subagent received the skill and the new synthetic offline input `tests/fixtures/review-continuation/project.md`, without an expected answer. This was a scoped continuation test with an existing issue summary, not a blind final review or a fourth reviewer of the result packet.

Observed behavior:

- Recommended closing the candidate after the initial failure and two repairs; retained the same family/count for a display-name change. Did not grant a third repair or automatic new pilot.
- Kept a materially different future mechanism conditional on actual evidence, module review, remaining global resources and deadline. Did not invent that mechanism.
- Distinguished a Crossref timeout from a successful zero-result response. Used the remaining supplied source transcript, retained unsearched coverage, and did not claim a live search.
- Linked preprint/conference/extended versions without hiding the extension's claimed regularization difference. Kept real citation identity unresolved and abstract-level support separate from unassessed full mechanisms.
- Preserved the existing issue ID and open status: recommending closure is not proof that the project ledger was changed. Recorded resolution tests and required recheck evidence.
- Calculated aggregate differences −1.0, −0.5 and −0.2 points without claiming prediction reconstruction or significance. Prioritized negative-result handoff within the original deadline.

No training, network, dependency installation, real paper-project mutation, publication or cross-chat message was part of these behavior checks.

## Limits / 验证边界

These are internal checks with synthetic inputs and explicit scope constraints. The primary executor arranged reviewer dispatch and the post-review audit; this does not validate autonomous orchestration in every future session. Actual literature-service fallback was not exercised: its interpretation was checked from the supplied offline transcript. Three reports were not an external peer review or proof of scientific originality.

Real-project intake, paper/code comparison, GPU experiments, process recovery, storage control, complete fair evidence and scientific effectiveness remain to be tested in the user's agreed research environment. Review approval, isolation, source verification, real resource use and scientific correctness remain procedural/project-tool responsibilities rather than new registry enforcement.
