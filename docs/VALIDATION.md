# Validation record and acceptance scope

**Version:** 0.2.0. **Date:** October 27, 2026. [简体中文](VALIDATION.zh-CN.md)

**v0.2.0 decision update.** See [the v0.2.0 validation record](VALIDATION-0.2.0.md) for research positioning and staged pilot-admission checks. The [v0.1.3 record](VALIDATION-0.1.3.md) and observations below retain their original version labels; previous software or behavior results are not presented as a new scientific benchmark.

This record distinguishes software validation, internal synthetic behavior checks, and real research acceptance. The first two have bounded completed checks; real-project effectiveness remains unvalidated.

Version 0.1.2 clarified the pilot-review gate and fixed control-experiment bookkeeping and self-referencing evidence. See the [audit record](AUDIT-2026-10-26.zh-CN.md) and [first project-pilot checklist](PILOT-TEST.zh-CN.md) (Chinese). The isolated behavior checks and internal code review below were conducted for v0.1.0; they are historical observations. The v0.1.2 update reran software/static checks and added nine unit/CLI regressions. Real-project behavior still requires project-pilot observation.

## Software and packaging

| Check | Recorded outcome |
| --- | --- |
| Official `skill-creator` static validation | Passed: `Skill is valid!`. |
| Python standard-library unit and CLI tests | 40 passed on Windows / Python 3.13.9, with no skips. |
| Relative links, Python/JSON parsing, and skill structure | Passed. |
| Standalone skill-directory relocation | CLI started from a temporary directory; the incomplete contract was correctly marked not ready. |
| Release-content inspection | Inspected the file manifest and searched for local user paths, original project identifiers, common credential patterns, and private-key markers; no matches found in the release files. |
| Release ZIP | Archive integrity and byte-for-byte agreement after extraction passed; `SHA256SUMS` supplied. |
| Published release assets | Downloaded uploaded ZIP and checksums and confirmed the expected digest. |
| GitHub Actions | Windows/Linux × Python 3.10/3.12. See [the actual runs](https://github.com/boji1334/ai-research-workflow/actions/workflows/validate.yml) for each revision's result. |

Local verification:

```text
python -m unittest discover -s tests -v
python tools/validate_repository.py
```

Test tasks and numerical values are synthetic fixtures for software and procedure behavior. They represent no real algorithm, dataset performance, or novelty evidence.

## Isolated-context behavior checks

A Codex subagent received the skill and raw fixtures for two scenarios without an expected answer. It performed no training, dependency installation, or access to the original research projects. The primary executor checked the returned behavior and calculations. This was an internal check with isolated context, not external peer review.

| Scenario and raw input | Observed response |
| --- | --- |
| `tests/fixtures/intake/project.md`: a missed-defect description with missing data roles, baseline results, and execution facts | Remained at project intake. Asked about task/artifacts, splits and batch isolation, allowed changes, and execution resources; deferred publication target and deadline until project facts were clarified. Proposed no module and started no training. |
| `tests/fixtures/result-review/`: a claimed stable gain from 80 to 82, all seeds, and different data/training budgets | Recomputed baseline mean 80.00, candidate mean 74.33, and mean difference −5.67 points. Retained the failed seed; identified extra synthetic data, doubled updates, missing module review, and missing ablations. Found the evidence insufficient for successful handoff. |

The second check recomputed CSV aggregates. Raw predictions were absent, so the agent did not claim to have recomputed AP. This distinction matches the skill's evidence requirements.

These checks establish observed behavior for this environment and these cases. They do not establish identical future behavior across all models and projects.

## Internal code review

A separate isolated-context Codex subagent reviewed the run registry and exercised it in temporary directories. Its first pass identified six issue classes; each was fixed and covered by regression tests:

| Issue class | Implemented correction |
| --- | --- |
| Symlink aliases could fork registry history | Canonicalize paths and reject registry files with multiple hard links. |
| Non-UTF-8 Windows output could fail after commit | Emit CLI JSON as UTF-8. |
| Initialization could expose partially written state | Write a complete temporary file, then publish atomically without replacing an existing target. |
| Corrupt histories could be accepted | Validate history order and completion evidence. |
| JSON exponent overflow could alter readiness | Reject non-finite JSON numeric values. |
| Extreme numeric and encoding errors behaved inconsistently | Return controlled input errors. |

The original reviewer reran the six reproductions against the corrected version and found no remaining failures in those reproductions. The 31 tests passed without skips. Checks included alias locking/history, forced GBK output, initialization write/publication faults, missing pilot/evidence history, exponent overflow, oversized integers, and invalid UTF-8.

The initial review also exercised three groups of four competing processes: identical fingerprint, identical candidate, and a total-run limit. Each group accepted only one registration. Subsequent write/replace fault injection preserved the previous registry. These checks used temporary files and did not simulate real training or scientific conclusions.

## Real research acceptance: outstanding

No user paper project or GPU training was started for this release. The following still require actual project validation:

1. Complete intake for a real vision research problem and establish an executable protocol and budget.
2. Check the mechanism against original papers and code and perform module review against the agreed publication target.
3. Complete a small implementation, training, evaluation, result-review, and archival cycle.
4. Verify interrupted-run recovery, actual process state, duplicate prevention, and resource management in that execution environment.
5. Complete necessary fair comparisons, ablations, stability/generalization/cost evidence, and final result review.

Research success requires those actual artifacts. Static checks, agent agreement, synthetic scenarios, software tests, and real scientific acceptance are reported separately.
