# Sweep Configuration Notes

This folder contains parameter sweep definitions for reproducible sensitivity experiments.

## Baseline Sweep Conventions

File: `baseline_sensitivity.json`

- `vary.victims.gmm_profile` selects a named profile key.
- `fixed.victims.gmm_profiles` maps each profile key to `std_xy` arrays.
- `fixed.victims.n_clusters` and `fixed.victims.weights` stay fixed during baseline sensitivity runs.

Rationale:
- Keeping cluster count and weights fixed avoids confounding the first policy/sensor/distribution sensitivity analysis.

Conditional usage:
- If `victims.distribution == uniform`, the selected `victims.gmm_profile` is ignored.

## Baseline Sweep Size

Current Cartesian product:
- 3 policies
- 2 victim distributions
- 2 sensor models
- 2 GMM profiles

Total configurations: `3 * 2 * 2 * 2 = 24`

With `runs_per_config = 30`, total runs are:
- `24 * 30 = 720`

## Full-Factorial ACO Sweep

File: `full_factorial_aco.json`

- `varAcoCandidateCount`: `12, 18, 24, 30, 36`
- `varAcoStepLength`: `50, 75, 100, 125, 150`
- `varAcoAlpha`: `0.5, 1.0, 1.5, 2.0, 2.5`
- `varAcoBeta`: `1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0`

Recommended replication:
- 3 seeds for validation
- 10 seeds for the full paper run

Total full-run size:
- `5 * 5 * 5 * 7 * 10 = 8750` runs