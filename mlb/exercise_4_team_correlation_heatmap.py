"""
Exercise 4: Team Performance Correlation Heatmap

Creates a correlation heatmap showing the relationship between team wins and various performance metrics:
- Runs scored
- Runs allowed
- Home runs
- Stolen bases
- Errors
- Team batting average
- Team ERA

Uses appropriate color scaling and annotations to show correlation coefficients.
"""

from dotenv import load_dotenv

load_dotenv()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from mlb.db import execute_query_with_validation


def load_team_performance_data() -> pd.DataFrame:
    """
    Load team performance data from the database.

    Returns:
        DataFrame with team performance metrics for correlation analysis
    """
    query = """
    SELECT 
        yearid,
        teamid,
        w as wins,
        r as runs_scored,
        ra as runs_allowed,
        hr as home_runs,
        COALESCE(sb, 0) as stolen_bases,
        e as errors,
        CAST(h AS FLOAT) / NULLIF(ab, 0) as batting_average,
        CAST(era AS FLOAT) as team_era
    FROM lahman."Teams" 
    WHERE ab > 0 AND era IS NOT NULL
    ORDER BY yearid DESC, teamid
    """

    print("Loading team performance data...")
    df = execute_query_with_validation(query)

    print(
        f"Loaded {len(df)} team seasons from {df['yearid'].min()} to {df['yearid'].max()}"
    )
    print(f"Data shape: {df.shape}")

    return df


def create_correlation_heatmap(df: pd.DataFrame) -> None:
    """
    Create a correlation heatmap showing relationships between team wins and performance metrics.

    Args:
        df: DataFrame with team performance data
    """
    # Select the metrics for correlation analysis
    correlation_metrics = [
        "wins",
        "runs_scored",
        "runs_allowed",
        "home_runs",
        "stolen_bases",
        "errors",
        "batting_average",
        "team_era",
    ]

    # Create correlation matrix
    correlation_data = df[correlation_metrics].copy()

    # Remove any rows with missing values
    correlation_data = correlation_data.dropna()

    print(f"Computing correlations for {len(correlation_data)} complete team seasons")

    # Calculate correlation matrix
    corr_matrix = correlation_data.corr()

    # Create the heatmap
    plt.figure(figsize=(12, 10))

    # Create a custom colormap - diverging from red (negative) through white to blue (positive)
    cmap = sns.diverging_palette(10, 220, as_cmap=True)

    # Create the heatmap with annotations
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap=cmap,
        center=0,
        square=True,
        fmt=".3f",
        cbar_kws={"label": "Correlation Coefficient"},
        annot_kws={"size": 10, "weight": "bold"},
    )

    # Customize the plot
    plt.title(
        "Team Performance Correlation Matrix\nRelationship Between Wins and Key Performance Metrics",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )

    # Improve label readability
    metric_labels = [
        "Wins",
        "Runs Scored",
        "Runs Allowed",
        "Home Runs",
        "Stolen Bases",
        "Errors",
        "Batting Average",
        "Team ERA",
    ]

    plt.xticks(range(len(metric_labels)), metric_labels, rotation=45, ha="right")
    plt.yticks(range(len(metric_labels)), metric_labels, rotation=0)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Save the plot
    output_path = "outputs/exercise_4_team_correlation_heatmap.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Correlation heatmap saved to: {output_path}")

    # Display correlation insights
    print("\n=== KEY CORRELATION INSIGHTS ===")

    # Focus on correlations with wins
    wins_correlations = (
        corr_matrix["wins"].drop("wins").sort_values(key=abs, ascending=False)
    )

    print(f"\nStrongest correlations with WINS:")
    for metric, correlation in wins_correlations.items():
        direction = "positive" if correlation > 0 else "negative"
        strength = (
            "very strong"
            if abs(correlation) > 0.7
            else "strong"
            if abs(correlation) > 0.5
            else "moderate"
            if abs(correlation) > 0.3
            else "weak"
        )
        print(
            f"  {metric.replace('_', ' ').title()}: {correlation:.3f} ({strength} {direction})"
        )

    # Highlight interesting relationships
    print(f"\n=== NOTABLE RELATIONSHIPS ===")

    # Runs scored vs batting average
    runs_ba_corr = corr_matrix.loc["runs_scored", "batting_average"]
    print(f"Runs Scored ↔ Batting Average: {runs_ba_corr:.3f}")

    # Runs allowed vs ERA
    ra_era_corr = corr_matrix.loc["runs_allowed", "team_era"]
    print(f"Runs Allowed ↔ Team ERA: {ra_era_corr:.3f}")

    # Home runs vs runs scored
    hr_runs_corr = corr_matrix.loc["home_runs", "runs_scored"]
    print(f"Home Runs ↔ Runs Scored: {hr_runs_corr:.3f}")

    # Errors vs wins (defensive impact)
    errors_wins_corr = corr_matrix.loc["errors", "wins"]
    print(f"Errors ↔ Wins: {errors_wins_corr:.3f}")


def analyze_data_quality(df: pd.DataFrame) -> None:
    """
    Analyze data quality and provide summary statistics.

    Args:
        df: DataFrame with team performance data
    """
    print("\n=== DATA QUALITY ANALYSIS ===")

    # Check for missing values
    missing_counts = df.isnull().sum()
    if missing_counts.sum() > 0:
        print("Missing values by column:")
        for col, count in missing_counts[missing_counts > 0].items():
            print(f"  {col}: {count} ({count / len(df) * 100:.1f}%)")
    else:
        print("No missing values found in the dataset")

    # Summary statistics
    print(f"\nDataset Summary:")
    print(f"  Total team seasons: {len(df):,}")
    print(f"  Years covered: {df['yearid'].min()} - {df['yearid'].max()}")
    print(f"  Unique teams: {df['teamid'].nunique()}")

    # Performance ranges
    print(f"\nPerformance Ranges:")
    print(f"  Wins: {df['wins'].min()} - {df['wins'].max()}")
    print(f"  Runs Scored: {df['runs_scored'].min()} - {df['runs_scored'].max()}")
    print(f"  Runs Allowed: {df['runs_allowed'].min()} - {df['runs_allowed'].max()}")
    print(
        f"  Batting Average: {df['batting_average'].min():.3f} - {df['batting_average'].max():.3f}"
    )
    print(f"  Team ERA: {df['team_era'].min():.2f} - {df['team_era'].max():.2f}")


if __name__ == "__main__":
    # Load the data
    team_data = load_team_performance_data()

    # Analyze data quality
    analyze_data_quality(team_data)

    # Create correlation heatmap
    create_correlation_heatmap(team_data)

    print("\n=== EXERCISE 4 COMPLETE ===")
    print("Team performance correlation heatmap has been generated successfully!")
