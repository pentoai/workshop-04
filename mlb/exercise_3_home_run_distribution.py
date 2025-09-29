"""
Exercise 3: Home Run Distribution by Decade

Creates a box plot showing the distribution of home runs per player by decade since 1920.
Only includes players with at least 1 home run in that decade.
"""

# MANDATORY first lines
from dotenv import load_dotenv

load_dotenv()

# Core imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Database (REQUIRED)
from mlb.db import execute_query_with_validation


def get_home_run_data():
    """
    Retrieve home run data aggregated by player and decade since 1920.
    Only includes players with at least 1 home run in each decade.
    """
    query = """
    SELECT 
        "playerID",
        FLOOR("yearID" / 10) * 10 as decade,
        SUM(CAST(COALESCE(NULLIF("HR", ''), '0') AS INTEGER)) as total_home_runs
    FROM lahman."Batting" 
    WHERE "yearID" >= 1920 
    GROUP BY "playerID", FLOOR("yearID" / 10) * 10
    HAVING SUM(CAST(COALESCE(NULLIF("HR", ''), '0') AS INTEGER)) >= 1
    ORDER BY decade, total_home_runs DESC
    """

    print("Executing query to retrieve home run data by decade...")
    df = execute_query_with_validation(query)
    print(f"Retrieved {len(df)} player-decade records")

    return df


def create_home_run_boxplot(df):
    """
    Create a horizontal box plot showing home run distribution by decade.
    """
    # Set up the plot style
    plt.style.use("default")
    sns.set_palette("husl")

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(14, 10))

    # Create the horizontal box plot
    box_plot = sns.boxplot(
        data=df,
        x="total_home_runs",
        y="decade",
        orient="h",
        ax=ax,
        showfliers=True,
        fliersize=3,
        linewidth=1.2,
    )

    # Customize the plot
    ax.set_title(
        "Home Run Distribution by Decade (1920-2020s)\nPlayers with ≥1 HR per Decade",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    ax.set_xlabel(
        "Total Home Runs per Player per Decade", fontsize=12, fontweight="bold"
    )
    ax.set_ylabel("Decade", fontsize=12, fontweight="bold")

    # Format y-axis labels to show decades properly
    decade_labels = [f"{int(decade)}s" for decade in sorted(df["decade"].unique())]
    ax.set_yticklabels(decade_labels)

    # Add grid for better readability
    ax.grid(True, alpha=0.3, axis="x")

    # Customize box plot appearance
    for patch in box_plot.artists:
        patch.set_alpha(0.7)

    # Add some statistics as text
    stats_text = []
    for decade in sorted(df["decade"].unique()):
        decade_data = df[df["decade"] == decade]["total_home_runs"]
        median_hr = decade_data.median()
        max_hr = decade_data.max()
        player_count = len(decade_data)
        stats_text.append(
            f"{int(decade)}s: {player_count} players, median={median_hr:.0f}, max={max_hr}"
        )

    # Add statistics text box
    stats_str = "\n".join(stats_text)
    ax.text(
        0.02,
        0.98,
        stats_str,
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
    )

    # Adjust layout
    plt.tight_layout()

    return fig


def analyze_home_run_trends(df):
    """
    Print analysis of home run trends across decades.
    """
    print("\n" + "=" * 60)
    print("HOME RUN DISTRIBUTION ANALYSIS BY DECADE")
    print("=" * 60)

    for decade in sorted(df["decade"].unique()):
        decade_data = df[df["decade"] == decade]["total_home_runs"]

        print(f"\n{int(decade)}s:")
        print(f"  Players with ≥1 HR: {len(decade_data):,}")
        print(f"  Median HRs per player: {decade_data.median():.1f}")
        print(f"  Mean HRs per player: {decade_data.mean():.1f}")
        print(f"  Max HRs (single player): {decade_data.max()}")
        print(f"  75th percentile: {decade_data.quantile(0.75):.1f}")
        print(f"  Players with 100+ HRs: {(decade_data >= 100).sum()}")
        print(f"  Players with 200+ HRs: {(decade_data >= 200).sum()}")

    # Overall trends
    print(f"\n" + "-" * 40)
    print("OVERALL TRENDS:")
    print("-" * 40)

    decade_medians = df.groupby("decade")["total_home_runs"].median()
    decade_means = df.groupby("decade")["total_home_runs"].mean()
    decade_counts = df.groupby("decade").size()

    print(
        f"Decade with highest median HRs: {int(decade_medians.idxmax())}s ({decade_medians.max():.1f})"
    )
    print(
        f"Decade with highest mean HRs: {int(decade_means.idxmax())}s ({decade_means.max():.1f})"
    )
    print(
        f"Decade with most players (≥1 HR): {int(decade_counts.idxmax())}s ({decade_counts.max():,} players)"
    )

    # Find the most prolific home run hitters by decade
    print(f"\n" + "-" * 40)
    print("TOP HOME RUN HITTERS BY DECADE:")
    print("-" * 40)

    for decade in sorted(df["decade"].unique()):
        top_player = df[df["decade"] == decade].nlargest(1, "total_home_runs")
        if not top_player.empty:
            player_id = top_player.iloc[0]["playerID"]
            home_runs = top_player.iloc[0]["total_home_runs"]
            print(f"{int(decade)}s: {player_id} ({home_runs} HRs)")


if __name__ == "__main__":
    print("Starting Exercise 3: Home Run Distribution by Decade Analysis")
    print("=" * 60)

    # Get the data
    df = get_home_run_data()

    # Analyze trends
    analyze_home_run_trends(df)

    # Create the visualization
    print(f"\nCreating box plot visualization...")
    fig = create_home_run_boxplot(df)

    # Save the plot
    output_path = "outputs/exercise_3_home_run_distribution.png"
    fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"Box plot saved to: {output_path}")

    # Close the figure to free memory
    plt.close(fig)

    print("\nExercise 3 completed successfully!")
    print("=" * 60)
