from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _pareto_front(df: pd.DataFrame) -> pd.DataFrame:
    points = df[["convergence_rate", "mean_ct"]].dropna().copy()
    points = points.sort_values(["convergence_rate", "mean_ct"], ascending=[False, True])
    pareto = []
    best_time = float("inf")
    for _, row in points.iterrows():
        if row["mean_ct"] <= best_time:
            pareto.append((row["convergence_rate"], row["mean_ct"]))
            best_time = row["mean_ct"]
    return pd.DataFrame(pareto, columns=["convergence_rate", "mean_ct"]).drop_duplicates()


def make_plots(exp_dir: Path) -> Path:
    analyses = exp_dir / "analyses"
    analyses.mkdir(exist_ok=True)

    out_dir = analyses / "presentation"
    out_dir.mkdir(exist_ok=True)

    grouped = pd.read_csv(analyses / "grouped_stats.csv")
    runs = pd.read_csv(exp_dir / "run_summary.csv")

    sns.set_theme(style="whitegrid", context="talk")

    # 1) Reliability map over candidate count x step length.
    piv = grouped.pivot_table(
        index="acoStepLength",
        columns="acoCandidateCount",
        values="convergence_rate",
        aggfunc="mean",
    )

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(
        piv,
        cmap="YlGnBu",
        vmin=0.5,
        vmax=1.0,
        annot=True,
        fmt=".2f",
        cbar_kws={"label": "Mean convergence rate"},
        ax=ax,
    )
    ax.set_title("Reliability Landscape: Step Length vs Candidate Count")
    ax.set_xlabel("Candidate count")
    ax.set_ylabel("Step length")
    fig.tight_layout()
    fig.savefig(out_dir / "heatmap_step_candidate_rate.png", dpi=220)
    plt.close(fig)

    # 2) Pareto-style view: convergence rate vs mean convergence time.
    fig, ax = plt.subplots(figsize=(10, 7))
    scatter = ax.scatter(
        grouped["convergence_rate"],
        grouped["mean_ct"],
        c=grouped["acoStepLength"],
        s=20 + grouped["acoCandidateCount"] * 2,
        cmap="viridis",
        alpha=0.8,
        edgecolors="none",
    )

    front = _pareto_front(grouped)
    if not front.empty:
        front = front.sort_values("convergence_rate")
        ax.plot(
            front["convergence_rate"],
            front["mean_ct"],
            color="crimson",
            linewidth=2.5,
            label="Pareto front",
        )

    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Step length")
    ax.set_title("Configuration Trade-off: Reliability vs Time")
    ax.set_xlabel("Convergence rate")
    ax.set_ylabel("Mean convergence time (s)")
    ax.set_xlim(0.45, 1.01)
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(out_dir / "scatter_rate_vs_time.png", dpi=220)
    plt.close(fig)

    # 3) Seed-level stability profile.
    by_seed = (
        runs.assign(converged=runs["converged"].astype(bool))
        .groupby("seed", as_index=False)
        .agg(
            convergence_rate=("converged", "mean"),
            mean_ct=("convergenceTime", "mean"),
            timeout_count=("converged", lambda x: (~x).sum()),
        )
    )

    fig, ax1 = plt.subplots(figsize=(10, 6))
    bars = ax1.bar(by_seed["seed"].astype(str), by_seed["convergence_rate"], color="#3B82F6", alpha=0.85)
    ax1.set_ylim(0.0, 1.0)
    ax1.set_ylabel("Convergence rate", color="#1D4ED8")
    ax1.set_xlabel("Seed")
    ax1.tick_params(axis="y", labelcolor="#1D4ED8")
    ax1.set_title("Seed Stability: Reliability and Timeouts")

    ax2 = ax1.twinx()
    ax2.plot(by_seed["seed"].astype(str), by_seed["timeout_count"], color="#DC2626", marker="o", linewidth=2)
    ax2.set_ylabel("Timeout count", color="#B91C1C")
    ax2.tick_params(axis="y", labelcolor="#B91C1C")

    for b in bars:
        h = b.get_height()
        ax1.text(b.get_x() + b.get_width() / 2, h + 0.015, f"{h:.2f}", ha="center", va="bottom", fontsize=8)

    fig.tight_layout()
    fig.savefig(out_dir / "seed_stability_profile.png", dpi=220)
    plt.close(fig)

    return out_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp-dir", required=True, help="Path to experiment folder containing run_summary.csv")
    args = parser.parse_args()

    exp_dir = Path(args.exp_dir)
    out = make_plots(exp_dir)
    print(f"Saved presentation plots to: {out}")


if __name__ == "__main__":
    main()
