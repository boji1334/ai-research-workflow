# Industrial Vision Research: design note

**Implementation:** v0.1.0 experimental skill. **Document date:** October 26, 2026.

This note describes the procedure implemented by the [skill](../skills/industrial-vision-research/SKILL.md), its optional run registry, and its current validation limits. It is project documentation. Research effectiveness on a real industrial vision project is an open validation task.

## 1. Problem and scope

The skill addresses a specific research workflow: a researcher has an industrial vision problem and needs to develop a defensible mechanism, determine whether it improves on fair baselines, and assemble sufficient experimental evidence for a stated publication goal.

The first version covers defect detection and localization, along with directly related few-shot and self-supervised research. It supports an existing project or a project whose facts are established through intake. Its terminal output is an experimental evidence package. Manuscript drafting and submission are separate follow-on requests.

The guiding principle is that a contribution must connect **a real bottleneck → a distinct mechanism → a testable prediction → observable evidence**. A renamed module, an isolated best seed, or a finished training command does not establish that chain.

## 2. Execution model

The implementation has three parts:

| Part | Actual responsibility |
| --- | --- |
| Skill instructions and references | Guide Codex's research decisions, intake, evidence collection, reviews, and handoff. |
| Codex and available project tools | Read sources, inspect and edit code, launch agreed experiments, inspect processes, and analyze actual artifacts. |
| Optional `research_guard.py` | Enforce structural contract and run-registration constraints using a local JSON registry. |

The skill package supplies no resident service, training engine, or scheduler. The research project supplies its actual environment, data, evaluation implementation, and job management. The registry's contents must be reconciled with real process state before resuming work.

The research lead, implementer, and reviewer are responsibilities, not a requirement for different model providers. Where supported, isolated Codex subagents can perform key reviews. Their output is identified as internal review with isolated context. Single-context self-review is recorded as such. Neither arrangement is described as external peer review.

## 3. Project intake and protocol

Intake first reads the existing project material, then asks only about unresolved requirements or facts. Project questions precede publication questions. The [intake reference](../skills/industrial-vision-research/references/intake.md) defines the relevant facts.

| Phase | Facts that must be established |
| --- | --- |
| Project | Task, current bottleneck, code and baseline, train/validation/test roles, prior attempts, fixed constraints, and allowed changes. |
| Resources | Execution target and owner, compute and storage budgets, active runs, and total run limit. |
| Publication | Target journal or level, access preference, applicable requirements, start date, deadline, and timezone. |
| Acceptance | Primary metric and direction, meaningful effect and rationale, planned repeats, fairness controls, and required evidence. |

The [contract template](../skills/industrial-vision-research/assets/research-contract.json) records these decisions. Structural completeness is checked by the helper; the facts and scientific adequacy require researcher and execution-context evidence.

### Publication target and acceptance

A top-tier SCI journal goal becomes a project-specific evidence contract informed by the target journal and relevant high-quality work:

- Compare the closest current mechanisms using their original papers and available implementations; state the search scope and unresolved neighbors.
- Use strong, relevant baselines with disclosed training, pretraining, external-data, evaluation, and tuning budgets.
- Judge the primary effect against observed variability and the task's practical value. Preserve all planned valid repeats and relevant class-level regressions.
- Use ablations and controls that distinguish the proposed mechanism from additional capacity, data, resolution, or optimization.
- Collect generalization and cost evidence where needed to support the actual claim.
- Confirm reproducibility and the limits of the conclusion from raw artifacts.

There is no fixed percentage-point threshold that implies top-tier readiness across tasks. A journal target does not establish global firstness or guarantee acceptance. The threshold, scope, and evidence are agreed for the project; approaching a deadline does not silently lower them.

## 4. Stages and artifacts

![Research workflow and bounded candidate loop](assets/research-loop.svg)

| Stage | Inputs | Required record | Decision |
| --- | --- | --- | --- |
| Intake | Existing project materials and user requirements | Resolved facts, remaining gaps, target, deadline | Clarify or establish protocol |
| Mechanism design | Failure evidence and closest prior work | Candidate family, hypothesis, differences, implementation path, distinguishing test | Enter module review |
| Module review | Candidate, original sources, code plan, protocol | Evidence-linked issues, impact, repair and uncertainty | Pilot, revise, known enhancement, or close |
| Pilot and bounded repair | Reviewed candidate and small-run budget | Code/config/data/seed identity, command, outputs, reviewed outcome | Expand evidence, justify repair, or close |
| Full experiments | Supported novelty and reviewed pilot gain | Fair baselines, comparisons, necessary ablations and claim-specific evidence | Enter final result review |
| Result review | Raw results, code, evaluator, protocol and claim | Recomputed metrics, confounds, stability, gaps, review verdict | Complete evidence or bounded follow-up |
| Handoff | Evidence and review records | Reproduction entrypoint, artifacts, supported claims, negative results, limits | Research success or partial delivery |

Projects can reuse their existing ledger and artifact layout. These are information requirements; they do not require a second competing directory structure. The [candidate](../skills/industrial-vision-research/assets/candidate.md) and [review](../skills/industrial-vision-research/assets/review.md) templates provide starting records.

## 5. Two scientific reviews

### Module review

Review the existence of the bottleneck, coverage of nearest prior work, mathematical or algorithmic differences, assumptions, and permitted information flow. Check whether tensor interfaces, gradients, training and inference paths are coherent and whether an experiment can distinguish the proposed explanation from obvious confounds.

Available decisions are `proceed_to_pilot`, `revise_before_pilot`, `known_enhancement`, and `close_candidate`. Passing this review means the candidate merits a bounded test. It does not prove novelty or a gain.

### Result review

Result review applies to pilot evidence before expanding experiments and to the full evidence package before accepting a contribution.

Inspect original predictions or logs, evaluation code, configuration, and the frozen protocol. Recompute the quantities supported by those artifacts. Check baseline strength, excluded runs, repeats, uncertainty, test-set use, weak classes, ablations, external information, and computational cost.

Available decisions are `evidence_complete`, `needs_bounded_followup`, `gain_without_supported_novelty`, and `unsupported_or_negative`. `evidence_complete` reports novelty support, performance acceptance, and required experiment coverage separately.

Every material finding locates evidence and states its effect on the claim, severity, smallest justified correction, and verification method. Reviewers receive the research question and actual artifacts without an expected verdict. Conflicting judgments are resolved against sources, recomputation, or a discriminating small test. Agreement alone is not empirical evidence.

**Current enforcement boundary:** the instructions require module and result review at key decisions. They do not mandate a new isolated review agent before every repair round, and the registry does not validate a review report's approval. Those distinctions remain explicit in v0.1.0. See the [review procedure](../skills/industrial-vision-research/references/review.md).

## 6. Negative results and bounded search

Candidate-level stopping and project-level stopping are separate decisions.

| Observation | Interpretation and action |
| --- | --- |
| Gain, insufficient novelty | Keep the engineering improvement with its proper attribution. Preserve the original baseline and compare against both in later work. Continue the mechanism search if resources remain. |
| Novelty support, no gain | Inspect implementation, gradient behavior, information flow, fairness, and the falsifiable mechanism prediction. A repair requires a specific evidence-based hypothesis and a bounded test. |
| Neither novelty nor gain | Close or reject the candidate when the evidence already refutes its basis; additional trials are not an entitlement. |
| Novelty support and preliminary gain | Complete the agreed evidence package before claiming research success. |
| New reproducible phenomenon contradicts the original hypothesis | Form and check a new hypothesis; preserve the original negative result. |

An initial pilot may be followed by **at most two small repair rounds**. Each round freezes one repair hypothesis and its total training budget. Replicate seeds or support sets belong to the round's preplanned total budget. The allowance can end earlier when the mechanism is refuted or resources run out.

The same mechanism retains its candidate-family identity across renaming, small parameter changes, and configuration splits. A closed candidate can be followed by a genuinely different mechanism within the fixed research question and remaining global budget. A fresh name or registry file does not reset history.

The helper conservatively consumes a repair slot when it is reserved, including a later cancelled or invalid run. A project that needs a more detailed infrastructure-failure policy must specify and retain it in its protocol. See [experiment rules](../skills/industrial-vision-research/references/experiments.md).

## 7. Run tracking and reproducibility

Associate each run with the protocol, code revision, data version, configuration, seed or support-set sampling, command, device, budget, logs, outputs, and checkpoint location. An evidence file must support the stated outcome. Preserve failures and cancelled work.

The optional registry offers `check-contract`, `init`, `reserve`, `finish`, and `status`. It freezes a contract digest, serializes updates using local file locking, rejects duplicate fingerprints, checks active candidate registrations and total run limits, and records evidence-file SHA-256 hashes. Initialization publishes a fully written registry without replacing an existing one on supported local filesystems.

The registry does not compute scientific metrics, inspect training processes, recognize equivalent mechanisms, meter GPU use, or validate a reviewer verdict. An evidence hash identifies bytes; it does not prove scientific correctness or provide tamper-proof auditing. Existing equivalent project tooling may be used instead. See [registry and recovery details](../skills/industrial-vision-research/references/state-and-delivery.md).

## 8. Completion and handoff

| State | Meaning |
| --- | --- |
| `candidate_closed` | A candidate has ended; the project may continue with a new mechanism. |
| `research_success` | Supported novelty, agreed gains, necessary evidence, and result review satisfy the project protocol. |
| `partial_delivery` | The deadline, resource boundary, or user-requested handoff arrives with unresolved research requirements. |

Estimate the remaining experimental and review work using observed run times. If the target appears out of reach, explain the gap early and ask whether the user wants to adjust the deadline or goal. Without an agreed change, deliver stage results at the original boundary. User instructions to stop or redirect also end the current plan.

Handoff includes source revision, reproducible configurations and commands, environment, raw result and checkpoint locations, comparisons and ablations, reviews, limitations, and negative results. Scientific success, software checks, and deadline compliance are reported separately.

## 9. Relationship to AI Scientist v3

[Sakana AI's AI Scientist v3](https://github.com/SakanaAI/AI-Scientist-v3) is associated with the October 13, 2026 arXiv preprint [*The Agentic Scientist*](https://arxiv.org/abs/2610.18933). The system uses staged research execution with coding agents and tracks artifacts across experimentation, evaluation, analysis, and manuscript production.

| Dimension | AI Scientist v3 | Industrial Vision Research v0.1.0 |
| --- | --- | --- |
| Packaging | Research pipeline and execution runtime | Codex skill, references, templates, optional run helper |
| Research scope | Computational research across tasks | Industrial vision, defect detection, related few-shot/self-supervised tasks |
| Starting point | Task description and task scaffold | Existing material plus project and publication intake |
| Execution | Pipeline drives configured coding agents and stages | Codex uses the tools and research environment available for the project |
| Endpoint | Includes manuscript generation | Experimental evidence handoff |
| Review emphasis | Staged verification; optional manuscript review | Mechanism and experimental-result review in the research procedure |
| Evaluation status | See the upstream paper and its evidence | Software/internal behavior checks completed; real-project effectiveness pending |

The adaptation takes inspiration from stage continuity, explicit evidence, and tracked research state. It does not integrate the v3 runtime or claim equivalent scientific results. The [provenance record](../skills/industrial-vision-research/references/sources.md) pins the inspected code revision and documents ARS, Orchestra Research, and K-Dense influences.

## 10. Validation and open work

The [validation record](VALIDATION.md) distinguishes static checks, 31 software tests, packaging, synthetic isolated-context checks, and internal code review. The CI matrix covers Windows/Linux and Python 3.10/3.12. These results validate the tested software behavior and specific procedure examples.

The next research validation task is a real industrial vision pilot: complete intake, check the mechanism against original sources, run small implementation and training checks, verify recovery and resource control, and audit fair comparisons and ablations. Scientific effectiveness remains unmeasured until those artifacts exist.

Potential stronger enforcement of review approvals should be evaluated against observed use. It is not a claimed capability of the current helper.
