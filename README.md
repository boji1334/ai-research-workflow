<p align="center">
  <img src="docs/assets/header.svg" alt="AI Research Workflow — a Codex skill focused on vision model research" width="100%">
</p>

<h1 align="center">AI Research Workflow</h1>

<p align="center">
  <strong>From a grounded research question to a reproducible experimental contribution.</strong><br>
  A Codex research skill focused on computer vision and vision models, including detection, segmentation, anomaly detection, and related few-shot and self-supervised learning.
</p>

<p align="center">
  <a href="https://github.com/boji1334/ai-research-workflow/actions/workflows/validate.yml"><img src="https://github.com/boji1334/ai-research-workflow/actions/workflows/validate.yml/badge.svg" alt="Software validation"></a>
  <a href="https://github.com/boji1334/ai-research-workflow/releases/tag/v0.1.2"><img src="https://img.shields.io/badge/release-v0.1.2%20preview-166b5b" alt="v0.1.2 preview"></a>
  <a href="skills/ai-research-workflow/scripts/research_guard.py"><img src="https://img.shields.io/badge/optional%20CLI-Python%203.10%2B-49647c" alt="Optional CLI: Python 3.10 or newer"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-49647c" alt="MIT License"></a>
</p>

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="#quickstart">Quickstart</a> ·
  <a href="#research-workflow">Workflow</a> ·
  <a href="docs/DESIGN.md">Design note</a> ·
  <a href="docs/VALIDATION.md">Validation</a> ·
  <a href="#citation">Citation</a>
</p>

AI Research Workflow gives Codex a research procedure: understand the existing project, agree on the publication target and budget, examine the closest prior work, implement a mechanism, run bounded experiments, and review the evidence. The workflow ends at an experimental handoff containing code, results, ablations, review records, and reproduction instructions.

**Status — experimental preview.** Software checks and isolated synthetic behavior checks are documented in the [validation record](docs/VALIDATION.md). End-to-end effectiveness on real vision research projects remains to be evaluated. Novelty, performance gains, and publication readiness require project evidence.

## What it adds

| Capability | Research behavior |
| --- | --- |
| **Project-grounded intake** | Read existing materials and resolve project facts first; then confirm the journal or publication level, access preference, and deadline. |
| **Mechanism-level novelty review** | Compare the closest papers, equations, supervision, and implementation paths. Separate a new mechanism from a renamed or known enhancement. |
| **Two scientific reviews** | Review the proposed module before a pilot and the observed results before expanding experiments or accepting a contribution. |
| **Bounded candidate search** | After an unsuccessful initial pilot, allow at most two justified small repair rounds. Close exhausted candidates and explore a different mechanism within the remaining budget. |
| **Evidence matched to the claim** | Plan strong baselines, fair comparisons, ablations, stability, generalization, and cost measurements around the actual contribution and publication target. |
| **Traceable continuation** | Preserve the project protocol, candidate history, run identities, raw artifacts, failures, reviews, and next action across sessions. |

## Quickstart

The [skill directory](skills/ai-research-workflow) contains the instructions, references, templates, and an optional Python helper. Install that directory into Codex; research runs use the execution environment agreed for your project. Docker and the upstream research frameworks are not dependencies of this skill.

### 1. Install the skill

If the official `skill-installer` is available in your Codex session:

```text
$skill-installer Install the skill from https://github.com/boji1334/ai-research-workflow/tree/main/skills/ai-research-workflow
```

Alternatively, download the standalone skill ZIP and `SHA256SUMS` from [Releases](https://github.com/boji1334/ai-research-workflow/releases). Extract the `ai-research-workflow` directory into your research project's `.agents/skills/` directory. The resulting entrypoint should be:

```text
YOUR_RESEARCH_PROJECT/.agents/skills/ai-research-workflow/SKILL.md
```

Compare versions before replacing an existing installation with local modifications. Start a new Codex session after installation. See the [official OpenAI skills documentation](https://developers.openai.com/codex/skills/) for skill discovery and scope.

### 2. Begin with your project

```text
$ai-research-workflow Take over this vision model research project.
Read the existing materials and ask about unresolved project facts first.
Then clarify my publication target and deadline before proposing experiments.
```

Provide access to the current code, dataset description and splits, baseline results, prior attempts, and execution resources that already exist. Missing facts are clarified during intake. Calling the skill starts this conversation; training follows an agreed project protocol.

### 3. Continue or request a review

```text
$ai-research-workflow Continue this research. Check the latest protocol,
active processes, candidate history, and review evidence before the next action.
```

```text
$ai-research-workflow Review this module against its closest prior work
and check whether the existing experiments support its mechanism. Review only.
```

Literature checks use the search and browsing tools available to Codex. Training uses your local or remote project environment, data access, compute, and storage budget. Codex subagents can review with isolated context when available; the review record identifies the actual arrangement.

## Research workflow

<p align="center">
  <img src="docs/assets/research-loop.svg" alt="Project intake and protocol; mechanism review and pilot; bounded repairs or candidate closure; full experiments and result review; experimental handoff at the agreed budget boundary" width="100%">
</p>

*Figure 1. The outer loop selects mechanisms; the inner loop tests a bounded repair hypothesis. Candidate closure preserves the research question and its remaining budget.*

1. **Establish the project.** Read the available evidence, resolve unknowns, and agree on the publication target, time, resources, and acceptance protocol.
2. **Select and review a mechanism.** Connect a real failure mode to a falsifiable hypothesis; inspect its closest prior work, implementation, and discriminating experiments.
3. **Run a small pilot.** Check the implementation and evaluation path before committing to full experiments. Investigate negative or ambiguous results using a specific repair hypothesis.
4. **Build the evidence.** After supported novelty, preliminary gain, and initial result review, complete the fair comparisons and contribution-specific experiments required by the protocol.
5. **Review and hand off.** Recompute what the raw artifacts support and report whether the research target was met, partially met, or remains unsupported.

The [design note](docs/DESIGN.md) specifies artifacts, review criteria, failure decisions, completion conditions, and the synthesis of research skills and methods.

### When does it stop?

| Situation | Next action |
| --- | --- |
| Gain with insufficient novelty | Preserve a known enhancement and its results; continue searching for a supported new mechanism. |
| Supported novelty, no gain | Review implementation, fairness, and the mechanism hypothesis; run up to two justified small repair rounds after the initial pilot. |
| Repairs exhausted or mechanism refuted | Close that candidate. A different mechanism may proceed within the original research scope and remaining resources. |
| Novelty, gains, required experiments, and result review all satisfy the protocol | Deliver the completed experimental evidence package. |
| Deadline or resource limit reached without an agreed extension | Deliver the actual stage results and unresolved gaps. |

A top-tier journal target raises the agreed evidence requirements; it does not establish a universal score increase or guarantee acceptance. See [publication-target criteria](docs/DESIGN.md#publication-target-and-acceptance).

## What you receive

The handoff ties the research claim to its supporting artifacts:

- Code revision, configuration, commands, environment, data roles, and evaluation protocol.
- Baseline and candidate results, all planned valid repeats, raw artifact and checkpoint locations.
- Relevant comparisons, ablations, mechanism tests, generalization, and computational costs.
- Module and result review records, negative results, limitations, and a reproduction entrypoint.

Research artifacts stay in the research project's agreed storage. This public repository distributes the skill and synthetic validation fixtures.

## Optional run registry

[`research_guard.py`](skills/ai-research-workflow/scripts/research_guard.py) uses the Python 3.10+ standard library. It checks contract structure, freezes a protocol digest, registers unique run fingerprints, limits repair slots, and records evidence-file hashes.

```text
python SKILL_DIR/scripts/research_guard.py check-contract --contract research-contract.json
python SKILL_DIR/scripts/research_guard.py status --registry research-runs.json
```

Replace `SKILL_DIR` with your installed skill directory. The [command reference](skills/ai-research-workflow/references/state-and-delivery.md) covers initialization, reservation, completion, and recovery.

The helper records runs; Codex and the project's execution tools launch them. Scientific judgments, actual process state, GPU hours, and storage quotas require separate verification. Review-report approval is currently a procedural responsibility rather than a CLI-enforced check.

## Documentation and validation

| Document | Purpose |
| --- | --- |
| [Design note](docs/DESIGN.md) | Scope, workflow, review logic, bounded iteration, and research-method synthesis. |
| [Validation record](docs/VALIDATION.md) | Completed software and internal behavior checks; outstanding research validation. |
| [Skill entrypoint](skills/ai-research-workflow/SKILL.md) | The procedure loaded by Codex. |
| [Design provenance](skills/ai-research-workflow/references/sources.md) | Upstream sources pinned to inspected revisions and the exact adaptation boundaries. |
| [Release notes and migration](docs/RELEASE-NOTES-0.1.2.md) | Versioned installation and release information. |
| [Changelog](CHANGELOG.md) | Changes to the repository. |
| [Pre-pilot audit](docs/AUDIT-2026-10-26.zh-CN.md) · [Pilot checklist](docs/PILOT-TEST.zh-CN.md) | Findings, fixes, and observable behavior for a first project pilot (Chinese). |

To verify the repository locally:

```text
python -m unittest discover -s tests -v
python tools/validate_repository.py
```

The current release has 40 software tests and a Windows/Linux × Python 3.10/3.12 CI matrix. Synthetic checks exercise intake and evidence review; they are distinct from algorithm benchmarks. See [validation details](docs/VALIDATION.md).

Near-term work focuses on one real project pilot, recovery checks in its execution environment, and evidence from fair comparisons and ablations before claiming research effectiveness.

## Research skills and methods

This skill synthesizes the following research skills and workflow methods into a unified procedure focused on vision research:

- [ARS-Codex · academic-research-suite](https://github.com/Imbad0202/academic-research-skills-codex): research-question clarification, staged progression, and source verification.
- [Orchestra Research · brainstorming-research-ideas](https://github.com/Orchestra-Research/AI-Research-SKILLs/tree/773a52944ba4747a18bd4ae9ade53fff041adcbc/21-research-ideation/brainstorming-research-ideas): research questions and mechanism hypotheses grounded in real bottlenecks.
- [Orchestra Research · autoresearch](https://github.com/Orchestra-Research/AI-Research-SKILLs/tree/773a52944ba4747a18bd4ae9ade53fff041adcbc/0-autoresearch-skill): inner and outer experiment loops, predefined protocols, and negative-result records.
- [K-Dense · scientific-critical-thinking](https://github.com/K-Dense-AI/scientific-agent-skills/tree/593377bb048752abb0152deab9fbb1083a6087df/skills/scientific-critical-thinking): evidence quality, confounds, mechanism explanations, and result review.
- [AI Scientist v3 · research workflow methods](https://github.com/SakanaAI/AI-Scientist-v3): stage continuity, run identities, and experimental-artifact tracking.

The [provenance record](skills/ai-research-workflow/references/sources.md) documents the synthesis and adaptation of each source.

## Citation

To reference this software, use the repository's **Cite this repository** entry or [`CITATION.cff`](CITATION.cff):

```bibtex
@software{ai_research_workflow_2026,
  author  = {{boji1334}},
  title   = {AI Research Workflow},
  version = {0.1.2},
  year    = {2026},
  url     = {https://github.com/boji1334/ai-research-workflow}
}
```

The [design note](docs/DESIGN.md) describes the current implementation and its limitations. This project has no accompanying research paper at this release.

Issues and contributions are welcome with a minimal, anonymized example and the relevant version. Keep private datasets, credentials, unpublished project details, and model weights in their agreed project storage.

[MIT License](LICENSE) applies to this repository's original content.
