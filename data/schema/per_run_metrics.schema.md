# Per-Run CSV Schema

Path pattern: `data/runs/<experiment_name>/<run_id>.csv`
Granularity: one row per simulation step.

## Columns
1. `run_id` - string
2. `experiment_name` - string
3. `seed` - integer
4. `step` - integer
5. `policy` - string (`greedy_nearest`, `lawnmower`, `partitioning`)
6. `sensor_model` - string (`probabilistic`, `deterministic`)
7. `n_uavs` - integer
8. `n_victims` - integer
9. `victims_found_cum` - integer
10. `new_detections_step` - integer
11. `coverage_ratio` - float in [0,1]
12. `redundancy_ratio` - float >= 0
13. `explore_count` - integer
14. `exploit_count` - integer
15. `return_count` - integer
16. `mean_battery` - float
17. `energy_used_cum` - float
18. `active_scans_step` - integer

## Notes
- Ratios should be computed consistently across all runs.
- Keep column order stable for notebook reproducibility.
