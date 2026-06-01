# New — 25/5

## New — 01/06 (Experiment log update)

**Validation sweep completed (3 seeds)**
Validation run folder: `src/UAV-SAR/experiments/20260601003108535/`

- Expected runs: `3 * 875 = 2625`
- Observed `run_summary.csv` rows: `2625`
- Converged runs: `2516` (`95.85%`)
- Timeouts: `109`

**Full factorial sweep completed (10 seeds)**
Full run folder: `src/UAV-SAR/experiments/20260601003651074/`

- Expected runs: `10 * 875 = 8750`
- Observed `run_summary.csv` rows: `8750`
- Converged runs: `8211` (`93.84%`)
- Timeouts: `539`

Analysis outputs were generated under each run folder in `analyses/`.
Additional presentation-focused figures for the full run were generated to:

- `src/UAV-SAR/experiments/20260601003651074/analyses/presentation/`
- `paper/UAV_SAR/img/experiments/`


**Startup dispersal**
UAVs now spread out before searching. Each UAV is assigned a starting waypoint (evenly spaced across the release zone) and must fly there before entering Explore. Sensing is active during dispersal so a victim spotted on the way in immediately switches the UAV to Exploit.

**Adaptive step uses minimum pheromone**
The decision to increase step length is now based on the *minimum* pheromone across all candidate directions rather than the average. The UAV only takes a longer jump when every nearby direction looks well-explored, not just most of them. This makes the adaptive step more conservative and avoids prematurely skipping over lightly-searched areas.

**Battery logic centralised**
Battery depletion is now owned by a single dedicated statechart running in parallel with the main behaviour statechart. Previously depletion was duplicated across every active state. Behaviour is unchanged; the model is easier to tune and reason about.

**UAVs spawn at full battery**
UAVs previously spawned with a random battery between 20 % and 80 %. They now always start at 100 %.

**FOV cone stays visible during charger transit**
The sensor cone was hidden whenever a UAV was heading to the charger. It now remains visible during the transit and only disappears while the UAV is physically docked and charging.

**FOV cone colour resets when heading to charger**
If a UAV detected a victim just before its battery dropped below the threshold, the cone stayed orange even while flying back to the charger. The cone now immediately returns to blue when a UAV enters the return-to-charger or charging phase.

**Victim placement now uses GMM**
The Gaussian mixture model placement function was implemented but never called, so victims were placed uniformly at random. Victims are now positioned according to the configured GMM clusters.

**Per-UAV state labels in the visualisation**
Two text labels below the release zone show the current behavioural state of each UAV (Startup / Explore / Exploit / To Charger / Charging) and update live during the simulation.

**Maximum simulation runtime extended**
The safety-stop timeout was raised from 100 s to 200 s, giving UAVs more time to find all victims before the run is marked as a timeout.

**Faster rendering**
The sensor cone visualisation was redrawn using coarser steps and slightly larger dots. The visual result is equivalent but the rendering is roughly 4× cheaper, noticeably reducing simulation lag at higher speeds.

---

# UAV-SAR — Recent progress and next steps

Summary (commit c802a72):
- Fixed UAV `Exploit` arrival behavior so agents re-sense and resume movement (prevents UAVs standing on victims).
- Added periodic sensing inside `Exploit` and visible UAV instance label in the UAV presentation.

Files changed (recent):
- `src/UAV-SAR/_alp/Agents/UAV/AOC.UAV.xml` — statechart/sensing changes
- `src/UAV-SAR/_alp/Agents/UAV/Levels/Level.level.xml` — UAV label and presentation tweaks
- `src/UAV-SAR/_alp/Agents/Main/EmbeddedObjects.xml` — population/replication adjustments
- `src/UAV-SAR/_alp/ModelResources.xml`

How to test locally
1. Close AnyLogic and delete the workspace cache if needed: `C:\Users\<you>\\.AnyLogicPLE\\Workspace8.*`.
2. Open the model in AnyLogic and build. Run a short simulation (2–5 minutes) and observe a few UAVs: confirm they no longer idle on top of victims and labels are visible.
3. Pause and inspect the following agent variables for a paused UAV: `varBatteryLevel`, `varMovingToCharger`, `varTargetConfidence`, `varVictimsConfirmed` and `varPheromoneGrid` sample cells.

Outstanding items / next work (priorities)
1. Investigate UAV charger behavior and battery thresholds (UAVs going to charger corners).
2. Verify and fix bottom UI panels (`Pheromone` and `Victim Placement`) bindings so values display.
3. Increase victim replication and run stress tests to confirm multi-UAV behavior.
4. Tune ACO / pheromone parameters if exploration/exploitation balance is off.
5. (Optional) Replace immediate resume with an Event-based short pause if UX requires a visible inspection delay.

Notes for reviewers
- Commit to review: c802a72 on branch `feature/fix-uav-victim-detection-logic`.

# UAV-SAR: Multi-Agent Search and Rescue System

## Overview

This project implements an agent-based UAV search and rescue (SAR) model.

Target architecture direction:
- BDI-style high-level state behavior
- ACO-inspired local coordination and movement selection
- TAPB-style belief freshness checks (Timed Active Perception Belief-TAPB)

Current objective is a stable, reproducible baseline that can be extended into full BDI+ACO+TAPB behavior and sensitivity experiments.

---

## Core Idea

Agents interact through a **shared environment** using:

* attraction to potential targets
* repulsion to avoid overlapping search

This enables emergent coordination and distributed exploration.

---

## Agent Behaviour

Each agent follows a general lifecycle:

* **Explore**: search the environment
* **Exploit**: investigate potential targets
* **Return**: manage resources (e.g. battery)
* **Adapt**: adjust behaviour under changing conditions

This reflects an exploration–exploitation trade-off in a dynamic environment.

---

## Current Implementation Status

Implemented and validated:
- AnyLogic model opens and runs from `src/UAV-SAR/UAV-SAR.alpx`.
- UAVs move continuously across the map area (bounded random waypoint baseline within the active search region).
- UAV statechart has guarded Explore/Exploit transitions based on:
	- `varTargetConfidence` vs `varDetectionThreshold`
	- `varBatteryLevel` vs `varReturnBatteryThreshold`
- Victim spawning uses robust GMM placement with in-bounds rejection/fallback.
- Simulation stop behavior is stable (no dynamic-event destruction errors in the current baseline flow).

Not fully implemented yet:
- TAPB stale-belief cycle (`SenseIfOutdated` as a full reasoning step).
- ACO local move scoring as the primary Explore policy (current movement baseline is bounded random waypoint chaining).
- Full experiment logging/export pipeline execution and result analysis automation.

---

## How To Run (AnyLogic)

### Prerequisites

- AnyLogic 8.9.x installed.
- Repository cloned locally.

### Run Steps

1. Open AnyLogic.
2. Open project file: `src/UAV-SAR/UAV-SAR.alpx`.
3. Open experiment: `Simulation`.
4. Click **Run**.
5. Observe UAV movement and victim interactions in the animation window.

Notes:
- Simulation experiment stop option is `Never`; stop manually when needed.
- Experiment uses fixed seed (`500000`) for baseline reproducibility.

Tuning (quick experiment knobs):
- In the Main agent Variables, adjust: 
  `varUseAcoMoveDefault`, `varAcoCandidateCountDefault`,
  `varAcoStepLengthDefault`, `varAcoUavAvoidRadiusDefault`, `varUavPushRateDefault`,
  `varRandomWeightDefault`, `varSensorRangeDefault`, `varBeliefStaleSecondsDefault`.

---

## Key Config And Data Paths

- Example experiment: `config/example_experiment.json`
- Baseline sensitivity sweep: `config/sweeps/baseline_sensitivity.json`
- Sweep conventions: `config/sweeps/README.md`
- Per-run/aggregate schema docs: `data/schema/`

---

## Project Structure

- `src/UAV-SAR/UAV-SAR.alpx`: AnyLogic workspace file
- `src/UAV-SAR/_alp`: generated AnyLogic source
- `src/UAV-SAR/_alp/Agents/Main/Code/Functions.java`: victim GMM placement
- `src/UAV-SAR/_alp/Agents/UAV/AOC.UAV.xml`: UAV startup + statechart guards
- `src/UAV-SAR/_alp/Agents/UAV/Code/Functions.java`: UAV waypoint movement callbacks
- `docs/`: planning and method notes
- `config/`: experiment/sweep definitions

---

## How to run experiments

You run the experiments in Anylogic (this will generate verbose log files) and later analyse them (summarize results and generate plots) using analyse.py

### In Anylogic

1. First decide which variables you want to test in the experiment (the experiment is currently set up to test varSensorRange, varAcoCandidateCount, varAcoStepLength, varAcoALpha, varAcoBeta, varSeed). 
2. Adding parameters is easy, in the main window, you add a parameter (not variable) for the variable you want to test. most likely this will be a variable in the uav agent, but the parametersweep experiment can only vary parameters in main. so we must define them in main and then manually sync them to uav later (see 3.)
3. In onStartup in the main agent, sync the parameter value you defined to the right variable in the uav agent:
```java
for (UAV u : uavs) {
    u.varSensorRange       = varSensorRange;
    u.varAcoCandidateCount = varAcoCandidateCount;
    u.varAcoStepLength     = varAcoStepLength;
    u.varAcoAlpha          = varAcoAlpha;
    u.varAcoBeta           = varAcoBeta;
    u.varBatteryLevel      = uniform(20, 80);
}
```
4. In the project side bar, double click "ExpParamSweep: Main" and go to the parameter section, here you define which parameter is part of the experiment, what is the minimum value, maximum value and the step size. the experiment will do a grid search through this parameter space. so keep the step size reasonably large so that the search space doesn't blow up.
5. right click the "ExpParamSweep: Main" in the left side bar and click run. this will generate the csv log files. 
6. once the experiment is running, it will do all the rest for you. it will automatically create a new directory under src/UAV-SAR/experiments/ with a digits-only timestamp (for example 20260517164951732). each experiment gets two files in their folder: run_summary.csv and victim_log.csv. run_summary.csv will get one line per run, that line will include all the parameter values, seed number, convergence time, ... the victim_log.csv file is more detailed and will have one line for every victim that is found in each run.
7. to analyse these results you run:
```bash
python analyse.py --base "src/UAV-SAR/experiments" --exp 20260517164951732
```
this command will create an analyses folder inside the experiment directory and place all the summary csv files and plots in there. you can also omit --exp to analyze the latest timestamped folder.
8. to generate other plots or summaries you will have to change the analyse.py file
9. if you want to sweep a variable from the main agent, simply convert it to a parameter and add it to the experiment like you did the other parameters. In anylogic, only parameters can be set from outside the model. you could also leave the variable and create a parameter with the same name and manually sync them in startup code if you prefer it that way.

---

## Next Technical Step

Replace random waypoint Explore movement with explicit TAPB + ACO decision flow:
1. Sense/refresh stale beliefs.
2. Score local movement options using ACO-style heuristic + pheromone terms.
3. Select and execute move, then deposit/update local trace.

This will align the running model with the intended research narrative for report and presentation.

---

## CI And Protection

The repo now includes a lightweight guard workflow:
- `.github/workflows/ci.yml` runs `scripts/check_alp_xml.py` on pushes and pull requests to `main`.
- The checker validates AnyLogic XML well-formedness, flags merge conflict markers, and catches empty `Code` blocks in the model files.

Recommended GitHub setting:
- Protect `main` and require the `AnyLogic Guard` workflow to pass before merge.

Note:
- A true AnyLogic headless simulation smoke test still needs an AnyLogic-enabled runner or a local manual run, so this workflow is the static safety gate rather than a full runtime replacement.

--- 

## Adaptive-step A/B study

Goal: compare the baseline against adaptive dynamic step sizing based on local pheromone average, using paired runs with the same seed in both modes.

Settings:
1. Baseline: `varUseAdaptiveStep = false`
2. Adaptive: `varUseAdaptiveStep = true`, `varAdaptiveStepThreshold = 1.25`, `varAdaptiveStepMaxMultiplier = 1.5`

Run artifacts and screenshots: [experiments-adaptive_stepsize](./experiments-adaptive_stepsize/)

| varSeed | Baseline (`false`) convergence time (s) | Adaptive (`true`) convergence time (s) |
|---|---:|---:|
| 23  | 65.75  | 125.80 |
| 1   | 73.25  | 128.00 |
| 35  | 156.75 | 66.70  |
| 176 | 190.45 | 97.90  |
| 69  | 88.80  | 102.10 |
| 5   | 100.62 | 91.50  |

### Result summary

- Adaptive is not uniformly better per seed (3 wins, 3 losses in this sample).
- Mean convergence improves from about `112.6s` to `102.0s`.
- Median is slightly worse with adaptive in this sample, so the gain comes from a few strong improvements rather than a universal shift.
- Because the same `varSeed` is used in both modes, each comparison is paired and aligned at the level of victim placement and stochastic decisions.

### Paper-ready takeaway

- Adaptive step is a promising opt-in heuristic.
- The effect is seed-sensitive.
- Default should remain conservative (`false`) until a larger paired sweep confirms the gain.

### Next validation step

1. Keep default `varUseAdaptiveStep = false` for stability, and only enable it for controlled experiments.
2. Expand to at least 30-50 paired seeds.
3. Sweep thresholds `1.10`, `1.25`, `1.50` with `varAdaptiveStepMaxMultiplier = 1.5`.
4. Report mean, median, success rate, and timeout count.
5. Promote adaptive step only if the larger sample preserves the improvement.

Charging note:
- Charger-bound movement now uses the same movement-speed setting as the other move paths, so heading to the charging station should not become a special fast path.
