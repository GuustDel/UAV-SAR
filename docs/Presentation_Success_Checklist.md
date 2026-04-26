# Presentation Success Checklist (H02H4a)

Use this checklist to maximize rubric score and presentation impact.

## 1. Storyline (3-minute overview)
1. Problem and intervention: what behavioural sensitivity are we testing?
2. Why agent-based modelling is appropriate here.
3. Local rules -> emergent outcomes.
4. Main result and one limitation.

## 2. Architecture Slide
1. Show environment, UAV agent, victim generation.
2. Show `Explore`, `Exploit`, `Return` intentions.
3. Explain sensor uncertainty and local-only information.
4. Show where randomness enters and how `seed` controls it.

## 3. Experiment Design Slide
1. Independent variables:
   - policy (`greedy_nearest`, `lawnmower`, `partitioning`)
   - victim distribution (`uniform` vs `gmm`)
   - sensor model (`probabilistic` vs `deterministic`)
2. Repeated runs: 30 seeds per configuration.
3. Key metrics: detection time, coverage efficiency, redundancy, energy.

## 4. Results Slide
1. Mean + variability across seeds.
2. At least one plot that compares policies under clustered victims.
3. One direct statement about emergent behaviour observed.

## 5. Reproducibility Slide
1. Show repo structure and where configs live.
2. Show where per-run and aggregate CSVs are stored.
3. Mention AnyLogic model file and exact seed usage.

## 6. Limitations and Next Step Slide
1. What is simplified (minimal model assumptions).
2. What may bias outcomes.
3. One realistic extension for future work.

## 7. Delivery Quality
1. Avoid over-technical text walls.
2. Use one key message per slide.
3. Keep transitions clean and timing rehearsed.

## 8. Peer-Evaluation Strategy
1. Keep a visible task board (who did what, when).
2. Record technical contributions per member (model logic, experiments, analysis).
3. Record packaging contributions per member (report, slides, narration).
4. Keep meeting notes and decisions to avoid ambiguity in peer scoring.

## 9. Statechart Justification Slide
1. Show baseline statechart (`Explore`, `Exploit`, `Return`) and why it was chosen.
2. Mention TAPB + ACO integration inside `Explore` (`SenseIfOutdated -> SelectMoveACO -> MoveAndDeposit`).
3. Briefly show advanced proposal (`Communication`, `Degraded`) as optional extension, not baseline.
4. Explicitly state that this choice reduces confounding and improves interpretability of sensitivity results.
