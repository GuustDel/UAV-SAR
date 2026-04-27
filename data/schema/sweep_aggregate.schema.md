# Sweep Aggregate CSV Schema

Path pattern: `data/sweeps/<sweep_id>_aggregate.csv`
Granularity: one row per completed run (seed x configuration).

## Columns
1. `run_id` - string
2. `experiment_name` - string
3. `seed` - integer
4. `policy` - string
5. `sensor_model` - string
6. `victim_distribution` - string (`uniform`, `gmm`)
7. `n_clusters` - integer
8. `cluster_std_descriptor` - string or compact JSON string
9. `detection_p0` - float
10. `detection_alpha` - float
11. `deterministic_radius` - float
12. `total_steps` - integer
13. `success_flag` - integer (`0` or `1`)
14. `time_to_all_found` - integer (`-1` if not all found)
15. `final_coverage_ratio` - float in [0,1]
16. `final_redundancy_ratio` - float >= 0
17. `total_energy_used` - float
18. `mean_battery_final` - float

## Notes
- This file is the primary source for sensitivity plots.
- Keep values scalar where possible for easy grouping in analysis notebooks.
