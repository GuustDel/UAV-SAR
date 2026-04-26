# ACO + BDI Formula Mapping (Project Justification)

This note links teammate literature extraction to the model decisions in this repository.

## Source Pointers
- `Literature Research related messages and links.md`
- `ACO_Formulas_Extracted_Image_2026-04-02_16.45.29.jpeg` extracted from this article; https://doi.org/10.1007/s00521-022-06998-9
Indepth analysis of ACO, PSO and ABC.
- `Project Context.md`
- `essay.tex`

## Extracted ACO Equations (teammate summary)

1. Node transition probability:

$$
p_{ij}^k = \frac{(\tau_{ij}^k)^\alpha (\eta_{ij}^k)^\beta}{\sum_{j \in N_i^k}(\tau_{ij}^k)^\alpha (\eta_{ij}^k)^\beta}
$$

2. Pheromone update/deposit + evaporation:

$$
\tau_{ij} = (1 - \rho)\tau_{ij} + \sum_{k=1}^{m}\Delta\tau_{ij}^k
$$

## How We Use Them in This Project

### In BDI terms
- Beliefs: local pheromone map + local target confidence + battery state.
- Desires: find victims, maximize coverage, avoid redundancy, preserve battery.
- Intentions: `Explore`, `Exploit`, `Return` (baseline), with TAPB checks before movement.

### In algorithmic terms
- During `Explore`, if beliefs are stale (TAPB outdated), perform active perception update.
- Then use node transition probability over neighboring candidates.
- `alpha` controls pheromone influence, `beta` controls heuristic influence.
- Apply evaporation/deposit every step to support stigmergic coordination.

## Minimal Parameter Set for Sensitivity Experiments
- `alpha` (pheromone weight)
- `beta` (heuristic weight)
- `rho` (evaporation/persistence effect)
- belief lifespan (TAPB duration)
- sensor model parameters (`p0`, `alpha_detect` or deterministic radius)

## Why This Fits Lecturer Intent
- Clear local rules produce emergent outcomes.
- Behaviour is traceable (statechart + explicit equations).
- Sensitivity can be tested systematically (parameter sweeps + multiple seeds).

## Scope Guardrail
Keep baseline simple first:
- robust spawning
- reproducible seeds
- clear Explore/Exploit/Return behavior

Treat advanced communication/failure handling as optional extension after baseline metrics are stable.