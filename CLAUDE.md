# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

AnyLogic agent-based simulation of multi-UAV search-and-rescue using a **reversed Ant Colony Optimisation** algorithm (pheromone repels rather than attracts). UAVs emit pheromone to mark recently-searched ground, steering each other toward unexplored area. Victims are placed via a Gaussian Mixture Model. The project is a research prototype producing CSV experiment data for a sensitivity analysis paper.

---

## Running the model

**Interactive simulation:**
1. Open `src/UAV-SAR/UAV-SAR.alpx` in AnyLogic 8.9.x.
2. Double-click `Simulation: Main` in the Projects panel → Run.

**Parameter sweep experiment (generates CSV output):**
1. Double-click `ExpParamSweep: Main` in the Projects panel.
2. Edit parameter ranges in the Parameters table (From / To / Step).
3. Right-click `ExpParamSweep` → Run.
4. Output lands in `src/UAV-SAR/experiments/<17-digit-timestamp>/` as `run_summary.csv` and `victim_log.csv`.

**Analyse results:**
```bash
python analyse.py                                         # latest experiment folder
python analyse.py --exp 20260517164951732                 # specific folder
python analyse.py --base "src/UAV-SAR/experiments" --exp 20260517164951732
```
Plots and summary CSVs are written to `experiments/<id>/analyses/`.

**Validate XML (CI gate):**
```bash
python scripts/check_alp_xml.py
```

---

## Architecture

### Agents

| Agent | Role |
|-------|------|
| `Main` | Orchestrator. Owns the shared pheromone grid, seeds RNG, pushes ACO parameters into each UAV, places victims via GMM, writes CSV logs. |
| `UAV` | Active search agent. Runs a hierarchical statechart + orthogonal battery drain loop. |
| `Victims` | Passive container. No behaviour. Marked found by Main when a UAV confirms detection. |

UAV instances hold a `main` ContainerLink giving direct access to `main.varPheromoneGrid`, `main.fnGetPheromone()`, etc.

### UAV statechart

Two parallel entry points:

**`stStartup` hierarchy** (main behaviour):
```
Startup → StartupMove (moveTo dispersal position)
  ↓ !isMoving()  [sets varStartupComplete = true]
Explore → ExploreSense → branch → [ExploreAdaptStep →] ExplorePlan → ExploreMove → (loop)
  ↓ varTargetConfidence ≥ 0.7
Exploit → ExploitVerify → ExploitApproach → ExploitConfirm → (loop back to Verify)
  ↓ confidence < threshold AND varStartupComplete
Explore  (or → ChargingStation if battery < 20 %)
ChargingStation → MovingToCharger → Charging → [battery = 100 %] → Explore
```

**`stBatteryDischarge`** (orthogonal, always active): cyclic 1 s self-loop, drains `0.5 %/s` unless `varMovingToCharger` or `varCharging`.

### Reversed-ACO scoring

`fnPickWaypoint()` places `varAcoCandidateCount` candidates on a ring of radius `varCurrentStepLength` and scores each:

```
s_i = (1 / (1 + τ_i))^α  ·  η_i^β
```

- `τ_i` = `main.fnGetPheromone(idx)` — lazy exponential decay `τ₀·e^(-ρ·Δt)`, ρ = 0.01
- `η_i` = `fnCellFreshness(idx)` = `max(0, (t − lastSensed) / 60)` — staleness heuristic
- Selection is proportional sampling over normalised scores.

Adaptive step (`varUseAdaptiveStep`): when `varMinCandidatePheromone ≥ 1.0`, scales the ring: `varCurrentStepLength = varAcoStepLength × min(2.0, 1 + τ_min)`.

### Pheromone grid

Shared in `Main`: 90 × 50 cells, 10 internal units/cell (1 m), origin at (50, 50). `varPheromoneGrid[]` stores deposited amounts; `varPheromoneTime[]` stores deposit timestamps. Evaporation is lazy — computed on-demand in `fnGetPheromone()`.

Per-UAV: `varCellLastSenseTime[]` and `varCellConfidence[]` (sized `main.varGridCols × main.varGridRows`) track each UAV's own belief about when it last sensed each cell.

### Source file layout

```
src/UAV-SAR/UAV-SAR.alpx          ← open this in AnyLogic
src/UAV-SAR/_alp/
  Agents/Main/
    AOC.Main.xml                   ← startup code, canvas, scale ruler
    Variables.xml                  ← all Main variables and parameters
    Code/Functions.xml             ← function signatures (fnPlaceVictimsGMM, fnGetPheromone, …)
    Code/Events.xml                ← eventDrawPheromones, eventSafetyStop
    EmbeddedObjects.xml            ← UAV and Victims replication counts
  Agents/UAV/
    AOC.UAV.xml                    ← full statechart with all entry actions and transitions
    Variables.xml                  ← all UAV variables
    Code/Functions.xml             ← function signatures (fnSenseNow, fnPickWaypoint, …)
  Agents/Victims/
    AOC.Victims.xml
    Variables.xml                  ← varIsFound, varFoundByUavIndex, varFoundAtTime
  Experiments.xml                  ← ExpParamSweep and Simulation experiment definitions
experiments/<timestamp>/
  run_summary.csv                  ← one row per run: seed, params, converged, convergenceTime
  victim_log.csv                   ← one row per victim found: params, victimIdx, uavIdx, foundTime, x, y
```

---

## Experiment setup rules

**All logic lives in statechart entry-actions and transition actions** (visible in `AOC.UAV.xml`). Function bodies in `Code/Functions.xml` are empty XML declarations — the implementations are compiled into the AnyLogic runtime.

**Adding a new swept parameter:**
1. Add a `Parameter` (not a plain Variable) to `Main/Variables.xml` or directly in AnyLogic's Main agent editor.
2. Sync it to UAV in Main's startup code: `for (UAV u : uavs) { u.varXxx = varXxx; }`.
3. Add it to `ExpParamSweep` in `Experiments.xml` (or via the AnyLogic UI: Parameters table, From/To/Step).
4. Add the column name to the CSV header in `Experiments.xml` `<InitialSetupCode>` and to the `fnLogRunSummary` / `fnLogVictimFound` write calls.
5. Add it to the `PARAMS` list in `analyse.py`.

**Seeds:** `varSeed` (40–60 range, 21 values) drives `getDefaultRandomGenerator().setSeed(varSeed)` at Main startup. All randomness (victim placement, waypoint selection) derives from this single seed.

**`varUseAdaptiveStep` must be `false` when sweeping `varAcoStepLength`** — otherwise the adaptive mechanism rescales the ring during the run and the configured step is not what is actually tested.

**Charger location** is hard-coded at `(880, 460)` in `MovingToCharger` entry action.

---

## Key parameter defaults

| Parameter | Default | Notes |
|-----------|---------|-------|
| `varAcoCandidateCount` | 24 | waypoints scored per step |
| `varAcoStepLength` | 80 | base ring radius (internal units ≈ metres × 10 scale) |
| `varAcoAlpha` | 1.0 | pheromone repulsion exponent |
| `varAcoBeta` | 2.0 | staleness attraction exponent |
| `varSensorRange` | 100 | detection radius |
| `varFovHalfAngleDeg` | 45 | forward cone half-angle |
| `varDetectionThreshold` | 0.7 | confidence to trigger Exploit |
| `varBeliefStaleSeconds` | 60 | staleness decay constant T |
| `varBatteryDepletionRate` | 1 | % per second (effective 0.5 %/s via 0.5× tick multiplier) |
| `varReturnBatteryThreshold` | 20 | % battery → go charge |
| `varChargingRate` | 10 | % per second while docked |
| `varMaxSimTime` | 200 | safety timeout (seconds) |
