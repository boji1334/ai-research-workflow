# Synthetic bounded-pilot admission packet

Everything below is synthetic. Use this packet and the assigned skill only. No network, training, installations, real project reads, repository edits or external messages. Write a review and next-action record only to the assigned evaluation directory.

## User request

“请审查这个候选是否值得做限定小试。已有审查意见也在下面，帮我确定哪些问题阻断什么阶段，并写清实验不同结果怎样处理。”

## Agreement and evidence scope

- Fixed task: supervised surface-defect segmentation, with a self-supervised pretraining stage on train images only. No new data or change in task, metric or split.
- Target is a defensible vision-method contribution; no named journal and no fixed universal AP gain. Primary downstream metric is validation mIoU. All scores are unmeasured for the candidate.
- One day remains. Six GPU-hours and one pilot batch remain, with no active processes or other reservations. Engineering preparation/review has a two-hour cumulative boundary, including earlier work. Forty minutes of that boundary have already been used. No future budget increase is agreed.
- Baselines A (original) and B (strong related enhancement) have verified same-protocol artifacts suitable for reuse. Model selection uses validation; final test is sealed. Source identity still needs checking if configurations change.
- The initial pilot plan contains one candidate and one same-capacity relation-shuffle ablation as subruns, with a fixed seed and total estimate four GPU-hours. The estimate is not a measured runtime. Baseline reuse avoids new baseline training if identity still matches. Pilot results alone do not complete research acceptance.

## Method and nearest neighbors

Supplied method excerpts are invented but complete for the limited comparison here. N1 uses a pooled global two-view consistency target. N2 uses independent local-patch matching, with no relation between two patches. Both use a known MLP projector and existing backbone.

Candidate C uses those same known components. On a fixed train-only grid it predicts the relative ordering of an image-derived two-patch contrast in both views. Targets are computed from training RGB before augmentation, detached, and their source-coordinate mapping follows the registered invertible crop. The auxiliary head is discarded before downstream fine-tuning. The full target/operator excerpt and shape diagram in this packet specify the two patch indices, the ordered pair label, a binary cross-entropy loss, shared encoder gradients and no test/label input. The supplied static checks establish matching tensor shapes and a connected gradient path; real gradient execution, noncollapse and save/reload are not yet checked. No leak or mathematical contradiction is demonstrated by the packet.

The relation-shuffle ablation keeps head size, images, patch sampling, optimizer budget and class-free label marginals, but permutes relation targets within each training minibatch using a fixed private RNG. C and the ablation use the same initialization and sample stream. This is one probe of the relation explanation, not proof of a unique causal mechanism. No claim is made that this relation has never appeared anywhere in the literature.

## Existing review comments (not decisions to adopt)

- R-01: “The MLP and encoder both have prior art, so the complete relation mechanism is necessarily identical to N1.”
- R-02: “There is no observed mIoU gain, multi-seed result or cross-dataset test yet; all experiments must wait until those are provided.”
- R-03: “The planned crop-coordinate and auxiliary-to-encoder gradient checks have not actually run.”
- R-04: “Even a successful single-seed relation ablation will not establish independent generalization or full novelty.”

No actual pilot, engineering check, test evaluation or registry mutation is requested as part of this review task. State the supported admission decision, scoped unresolved issues, minimum execution prerequisites and the predeclared meaning of positive, null, downstream-negative and engineering-failure outcomes. Respect the existing helper semantics and candidate/global budgets.
