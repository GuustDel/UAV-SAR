"""
UAV-SAR Experiment Analysis
Usage:
    python analyse.py              # analyses the latest numbered experiment
    python analyse.py --exp 2      # analyses experiments/2/
    python analyse.py --base path  # override base folder (default: experiments)
"""

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")

PARAMS = ["sensorRange", "acoCandidateCount", "acoStepLength", "acoAlpha", "acoBeta"]
PARAM_LABELS = {
    "sensorRange":      "Sensor Range",
    "acoCandidateCount":"ACO Candidate Count",
    "acoStepLength":    "ACO Step Length",
    "acoAlpha":         "ACO Alpha (α)",
    "acoBeta":          "ACO Beta (β)",
}

# ── helpers ──────────────────────────────────────────────────────────────────

FALLBACK_BASES = [
    Path("src/UAV-SAR/experiments"),
    Path("experiments"),
]

def resolve_base(base: Path) -> Path:
    if base != Path("experiments") and base.exists():
        return base
    for candidate in FALLBACK_BASES:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "Could not find an experiments folder. "
        "Run with --base pointing to the experiments directory, e.g.:\n"
        '  python analyse.py --base "src/UAV-SAR/experiments"'
    )


def find_latest(base: Path) -> Path:
    dirs = [d for d in base.iterdir() if d.is_dir() and d.name.isdigit()]
    if not dirs:
        raise FileNotFoundError(f"No numbered experiment directories in {base}/")
    return max(dirs, key=lambda d: int(d.name))


def load(exp_dir: Path):
    summary = pd.read_csv(exp_dir / "run_summary.csv")
    victims = pd.read_csv(exp_dir / "victim_log.csv")
    summary["convergenceTime"] = pd.to_numeric(summary["convergenceTime"], errors="coerce")
    summary["converged"] = summary["converged"].astype(bool)
    return summary, victims


def save(fig, out_dir: Path, name: str):
    path = out_dir / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {path.name}")

# ── plots ─────────────────────────────────────────────────────────────────────

def plot_marginal_convergence_time(summary: pd.DataFrame, out_dir: Path):
    converged = summary[summary["converged"]]
    fig, axes = plt.subplots(1, len(PARAMS), figsize=(20, 5), sharey=False)
    fig.suptitle("Convergence Time by Parameter (converged runs, averaged over all other params)", y=1.02)

    for ax, param in zip(axes, PARAMS):
        vals = sorted(converged[param].unique())
        data = [converged[converged[param] == v]["convergenceTime"].dropna().values for v in vals]
        bp = ax.boxplot(data, patch_artist=True, labels=[str(v) for v in vals])
        for patch in bp["boxes"]:
            patch.set_facecolor("steelblue")
            patch.set_alpha(0.6)
        ax.set_xlabel(PARAM_LABELS[param])
        if ax is axes[0]:
            ax.set_ylabel("Convergence Time (s)")
        ax.tick_params(axis="x", rotation=30)

    fig.tight_layout()
    save(fig, out_dir, "marginal_convergence_time.png")


def plot_marginal_convergence_rate(summary: pd.DataFrame, out_dir: Path):
    fig, axes = plt.subplots(1, len(PARAMS), figsize=(20, 4), sharey=True)
    fig.suptitle("Convergence Rate by Parameter (averaged over all other params)", y=1.02)

    for ax, param in zip(axes, PARAMS):
        grp = summary.groupby(param)["converged"].agg(["mean", "std", "count"]).reset_index()
        grp["se"] = grp["std"] / np.sqrt(grp["count"])
        ax.bar(grp[param].astype(str), grp["mean"], yerr=grp["se"],
                capsize=5, color="steelblue", alpha=0.7)
        ax.set_xlabel(PARAM_LABELS[param])
        ax.set_ylim(0, 1)
        if ax is axes[0]:
            ax.set_ylabel("Convergence Rate")
        ax.tick_params(axis="x", rotation=30)

    fig.tight_layout()
    save(fig, out_dir, "marginal_convergence_rate.png")


def plot_heatmap_pair(summary: pd.DataFrame, out_dir: Path,
                    row_param: str, col_param: str, filename: str):
    converged = summary[summary["converged"]]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"{PARAM_LABELS[row_param]} × {PARAM_LABELS[col_param]}")

    pivot_rate = (summary.groupby([row_param, col_param])["converged"]
                .mean().unstack())
    sns.heatmap(pivot_rate, ax=axes[0], annot=True, fmt=".2f",
                cmap="YlGn", vmin=0, vmax=1,
                cbar_kws={"label": "Convergence Rate"})
    axes[0].set_title("Convergence Rate")
    axes[0].set_xlabel(PARAM_LABELS[col_param])
    axes[0].set_ylabel(PARAM_LABELS[row_param])

    pivot_time = (converged.groupby([row_param, col_param])["convergenceTime"]
                .mean().unstack())
    sns.heatmap(pivot_time, ax=axes[1], annot=True, fmt=".0f",
                cmap="YlOrRd_r",
                cbar_kws={"label": "Mean Convergence Time"})
    axes[1].set_title("Mean Convergence Time (converged runs)")
    axes[1].set_xlabel(PARAM_LABELS[col_param])
    axes[1].set_ylabel(PARAM_LABELS[row_param])

    fig.tight_layout()
    save(fig, out_dir, filename)


def plot_victim_discovery_order(victims: pd.DataFrame, out_dir: Path):
    run_cols = PARAMS + ["seed"]
    victims_s = victims.sort_values(run_cols + ["foundTime"])
    victims_s["rank"] = (victims_s.groupby(run_cols).cumcount() + 1)

    agg = (victims_s.groupby("rank")["foundTime"]
            .agg(mean="mean", std="std", count="count").reset_index())
    agg["se"] = agg["std"] / np.sqrt(agg["count"])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(agg["rank"], agg["mean"], yerr=agg["se"], capsize=5,
            color="steelblue", alpha=0.75)
    ax.set_xticks(agg["rank"])
    ax.set_xlabel("Victim Discovery Order (1st found → last found)")
    ax.set_ylabel("Mean Discovery Time ± SE")
    ax.set_title("Average Time to Discover Each Victim Across All Runs")
    fig.tight_layout()
    save(fig, out_dir, "victim_discovery_order.png")


def plot_timeout_breakdown(summary: pd.DataFrame, out_dir: Path):
    """Show how many runs timed out vs converged, broken down by parameter."""
    fig, axes = plt.subplots(1, len(PARAMS), figsize=(20, 4), sharey=True)
    fig.suptitle("Timed-out Runs by Parameter Value", y=1.02)

    for ax, param in zip(axes, PARAMS):
        grp = summary.groupby(param)["converged"].value_counts(normalize=True).unstack(fill_value=0)
        if True not in grp.columns:
            grp[True] = 0
        if False not in grp.columns:
            grp[False] = 0
        grp = grp.reset_index()
        vals = grp[param].astype(str)
        ax.bar(vals, grp[False], label="Timed out", color="tomato", alpha=0.8)
        ax.bar(vals, grp[True], bottom=grp[False], label="Converged", color="steelblue", alpha=0.8)
        ax.set_xlabel(PARAM_LABELS[param])
        if ax is axes[0]:
            ax.set_ylabel("Fraction of runs")
            ax.legend()
        ax.tick_params(axis="x", rotation=30)

    fig.tight_layout()
    save(fig, out_dir, "timeout_breakdown.png")

# ── tables ────────────────────────────────────────────────────────────────────

def save_tables(summary: pd.DataFrame, out_dir: Path):
    converged = summary[summary["converged"]]

    # Full grouped stats
    agg = summary.groupby(PARAMS).agg(
        n_runs=("seed", "count"),
        convergence_rate=("converged", "mean"),
        mean_ct=("convergenceTime", lambda x: x.dropna().mean()),
        std_ct=("convergenceTime", lambda x: x.dropna().std()),
        median_ct=("convergenceTime", lambda x: x.dropna().median()),
        mean_victims=("victimsFound", "mean"),
    ).reset_index()
    agg.to_csv(out_dir / "grouped_stats.csv", index=False)
    print(f"  saved grouped_stats.csv  ({len(agg)} combinations)")

    # Top 20 by mean convergence time (fully converged combinations only)
    top = (agg[agg["convergence_rate"] == 1.0]
            .sort_values("mean_ct")
            .head(20))
    top.to_csv(out_dir / "top20_full_convergence.csv", index=False)
    print(f"  saved top20_full_convergence.csv  ({len(top)} combinations with 100% convergence rate)")

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp",  default=None, help="Experiment number, e.g. 1")
    parser.add_argument("--base", default="experiments", help="Base folder")
    args = parser.parse_args()

    base = resolve_base(Path(args.base))
    exp_dir = base / args.exp if args.exp else find_latest(base)

    if not exp_dir.exists():
        print(f"Not found: {exp_dir}")
        sys.exit(1)

    print(f"Experiment : {exp_dir.resolve()}")
    summary, victims = load(exp_dir)
    print(f"Runs       : {len(summary)}")
    print(f"Converged  : {summary['converged'].sum()} ({summary['converged'].mean():.1%})")
    print(f"Victim events: {len(victims)}")

    out_dir = exp_dir / "analyses"
    out_dir.mkdir(exist_ok=True)
    print(f"Output     : {out_dir.resolve()}\n")

    plot_marginal_convergence_time(summary, out_dir)
    plot_marginal_convergence_rate(summary, out_dir)
    plot_heatmap_pair(summary, out_dir, "acoAlpha", "acoBeta", "heatmap_alpha_beta.png")
    plot_heatmap_pair(summary, out_dir, "sensorRange", "acoStepLength", "heatmap_sensor_step.png")
    plot_heatmap_pair(summary, out_dir, "sensorRange", "acoCandidateCount", "heatmap_sensor_candidates.png")
    plot_victim_discovery_order(victims, out_dir)
    plot_timeout_breakdown(summary, out_dir)
    save_tables(summary, out_dir)

    print("\nDone.")

if __name__ == "__main__":
    main()