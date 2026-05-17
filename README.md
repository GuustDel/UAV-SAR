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
