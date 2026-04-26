# Statechart Alignment Review

This note evaluates teammate statechart artifacts against course intent and our BDI+TAPB+ACO project logic.

## Sources Reviewed
- `MAS___ACO-1.pdf`
- `UAV-SAR/docs/StateChart_Proposal_Guust.pdf`
- `UAV-SAR/docs/StateChart_Proposal_Arthur.pdf`
- `Project Context.md`
- `essay.tex`
- Course rubric and lecture themes (behavioural sensitivity, emergence, traceable local rules)

## Alignment Verdict

### 1) Guust / MAS___ACO-1 statechart
Status: aligned as baseline.

Why it fits:
- Clear minimal lifecycle: `Explore -> Exploit -> Return Base`.
- Naturally supports exploration-exploitation trade-off.
- Easy to explain and defend in a 6-page project + presentation.

What is missing for full project alignment:
- Explicit TAPB logic (stale beliefs trigger active perception).
- Explicit ACO move-selection step inside exploration.

### 2) Arthur statechart (Communication + Degraded)
Status: partially aligned, but too advanced for baseline.

Strengths:
- Good realism and robustness framing.
- Useful for discussion and possible extension experiments.

Risks for current scope:
- Increases implementation complexity and debugging risk.
- Can dilute the core behavioural sensitivity narrative if introduced too early.

## Recommended Project Decision
1. Use Guust/MAS___ACO-1 as the implementation baseline.
2. Enhance baseline by adding explicit internal Explore cycle:
   - `SenseIfOutdated` (TAPB)
   - `SelectMoveACO`
   - `MoveAndDeposit`
3. Keep `Communication` and `Degraded` as optional v2 extensions only after baseline results are reproducible.

## How to Use This in Justification and Presentation
- Show that the team considered both minimal and advanced architectures.
- Justify choosing minimal baseline using lecture guidance:
  - simple local rules,
  - traceable behaviour,
  - interpretable experiments,
  - clear emergence narrative.
- Present Communication/Degraded as future work or bonus sensitivity experiments.

## Suggested Slide Line
"We intentionally prioritized a minimal, traceable statechart for reproducible behavioural sensitivity experiments, then scoped communication/failure handling as optional extensions to avoid confounding effects in the core analysis."