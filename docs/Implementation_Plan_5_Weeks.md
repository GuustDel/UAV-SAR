# 5-Week Implementation Plan (AnyLogic UAV-SAR)

## Submission Target
- Final due time: 2026-06-08 morning (UTC+2)
- Deliverables due together:
  - Runnable AnyLogic model package
  - Article (max 6 pages)
  - Presentation deck

## Success Gates
1. Baseline model is reproducible from config + seed.
2. Core behavior is traceable: Explore/Exploit/Return logic and TAPB stale-belief checks.
3. Sensitivity experiments show clear behavioral differences.
4. Paper and slides tell one coherent story from local rules to emergent outcomes.

## Week-by-Week Plan

### Week 1 (2026-04-26 to 2026-05-03)
Goal: lock baseline architecture and reproducibility pipeline.

Model tasks:
- Finalize config key contract for environment, victims, sensor, and policy.
- Keep Guust baseline statechart as main flow and add guard conditions.
- Add deterministic seed plumbing for repeatable runs.

Experiment tasks:
- Run a smoke baseline with fixed seed and collect first run logs.
- Validate logging columns against `data/schema/per_run_metrics.schema.md`.

Writing/presentation tasks:
- Freeze one-paragraph problem statement and one-paragraph method summary.
- Prepare 2 backup slides: architecture rationale and baseline-vs-extension decision.

Definition of done:
- One baseline run is reproducible twice with same output summary.
- Config file and logging schema are internally consistent.

### Week 2 (2026-05-04 to 2026-05-10)
Goal: complete core agent behavior implementation.

Model tasks:
- Implement TAPB belief freshness checks (`SenseIfOutdated`).
- Implement ACO move scoring/selection using current local beliefs.
- Implement movement + pheromone update + battery consumption loop.

Experiment tasks:
- Verify behavior sanity with short visual runs.
- Record first per-run KPIs: coverage, detections, false alarms, distance, energy.

Writing/presentation tasks:
- Draft method section figures (statechart + formula mapping table).

Definition of done:
- Explore/Exploit transitions are driven by model variables, not fixed alternation.
- KPI logs generated for at least 10 seeded runs.

### Week 3 (2026-05-11 to 2026-05-17)
Goal: stabilize experiment harness and run baseline sensitivity sweep.

Model tasks:
- Wire sweep config ingestion for policy/distribution/sensor variations.
- Add per-run aggregate export compatible with `data/schema/sweep_aggregate.schema.md`.

Experiment tasks:
- Execute `baseline_sensitivity.json` sweep.
- Re-run selected points for repeatability checks.

Writing/presentation tasks:
- Draft results section skeleton with placeholders for plots/tables.

Definition of done:
- First full sweep completes without manual intervention.
- Repeatability check is documented.

### Week 4 (2026-05-18 to 2026-05-24)
Goal: analyze results and lock the core narrative.

Model tasks:
- Fix only critical behavior bugs (no feature creep).
- Optional v2 branch only if baseline is stable: communication/degraded experiments.

Experiment tasks:
- Produce final plots/tables for policy and environment sensitivity.
- Identify 2-3 strongest emergent behavior findings.

Writing/presentation tasks:
- Complete full article draft (all sections).
- Build full presentation draft with evidence-first structure.

Definition of done:
- Complete draft article and slide deck exist.
- Main claims are directly supported by experiment outputs.

### Week 5 (2026-05-25 to 2026-06-01)
Goal: final quality pass and rehearsal-ready delivery.

Model tasks:
- Freeze model behavior and config set.
- Verify clean rerun instructions from scratch.

Experiment tasks:
- Regenerate final figures/tables from frozen config/seed set.
- Archive run artifacts and metadata.

Writing/presentation tasks:
- Polish article to <= 6 pages and tighten references.
- Rehearse presentation with timing, Q&A, and backup slide flow.

Definition of done:
- Final submission package is complete and reproducible.
- Team can explain assumptions, trade-offs, and limitations clearly.

## Final Buffer (2026-06-02 to 2026-06-07)
- No new features.
- Only submission packaging, typo fixes, rerun verification, and final rehearsal.

## Immediate Next Steps
1. Keep `config/sweeps/baseline_sensitivity.json` consistent and implementation-ready.
2. Add TAPB + ACO behavior update loop in model code.
3. Add run logging hooks and verify schema alignment with one seeded run.