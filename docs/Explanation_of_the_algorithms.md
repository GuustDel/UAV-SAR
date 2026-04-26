Brief explanations of the three policies:

- greedy_nearest  
  - What: Each UAV repeatedly selects and moves to the nearest unsearched location or nearest high-value candidate (e.g., nearest unvisited cell or estimated victim).  
  - How: local perception (or shared visited map) → pick argmin(distance) → move → scan → optionally broadcast detection.  
  - Pros: simple, reactive, fast at finding isolated targets.  
  - Cons: causes agent clustering/redundant coverage, poor global coordination, possible oscillations.  
  - Key params: search cell size, communication/shared-visited flag, randomness/tie-breaking, lookahead radius.  
  - Tiny pseudocode:
    - candidates = local_unvisited_cells()
    - target = argmin_distance(candidates) + tie_break_noise
    - move_to(target); scan(); broadcast_if_found()

- lawnmower  
  - What: Systematic back-and-forth transect coverage (parallel swaths) that guarantees area coverage.  
  - How: precompute parallel sweep path using swath width ≈ sensor footprint; follow waypoints sequentially, scanning continuously.  
  - Pros: predictable, simple baseline with full coverage guarantee for static environments.  
  - Cons: inefficient for clustered or temporally-varying targets; no adaptivity to detected clusters unless augmented.  
  - Key params: swath width (sensor range), heading orientation, overlap fraction, waypoint spacing.  
  - Tiny pseudocode:
    - path = compute_lawnmower_path(swath_width)
    - for waypoint in path: move_to(waypoint); scan()

- partitioning  
  - What: Spatially split the environment into disjoint regions (grid, Voronoi based on UAV positions) and assign each UAV to search its region (using local policy like lawnmower or greedy inside the partition).  
  - How: compute partitions (static or dynamic), each UAV executes local search; optionally periodic load balancing/reassignment via local broadcasts.  
  - Pros: reduces inter-agent overlap, scales well with agent count, encourages fair workload division — good for clustered distributions.  
  - Cons: needs partitioning logic and some communication; poor if clusters cross partition boundaries unless dynamic reassignment is used.  
  - Key params: partition method (grid/Voronoi), reassignment frequency, local policy inside partition, commRange.  
  - Tiny pseudocode:
    - partitions = compute_partitions(uav_positions)
    - for each UAV: local_policy.search(partition[uav_id])
    - periodically: evaluate_load(); if imbalance -> reassign_partitions()

Quick experimental guidance
- Use lawnmower as deterministic coverage baseline (best for uniform distributions).  
- Use greedy_nearest to test reactive performance on sparse or few-target scenarios (expect clustering).  
- Use partitioning for multi-agent scalability and clustered distributions — combine with local reassignment to observe emergent load‑balancing.