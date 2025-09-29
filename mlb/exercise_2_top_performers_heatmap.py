#!/usr/bin/env python3
"""
Exercise 2: Top Performers Heatmap
Create a heatmap showing the top 10 home run hitters by decade.
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


def get_top_hr_hitters_by_decade() -> pd.DataFrame:
    """
    Query the database to get top 10 home run hitters by decade.

    Returns:
        DataFrame with columns: decade, player_name, total_hr, rank
    """
    query = """
    WITH decade_hr AS (
      SELECT 
        b."playerID",
        FLOOR(b."yearID" / 10) * 10 AS decade,
        SUM(CASE WHEN b."HR" IS NOT NULL AND b."HR" != '' THEN CAST(b."HR" AS INTEGER) ELSE 0 END) AS total_hr
      FROM lahman."Batting" b
      WHERE b."yearID" >= 1900  -- Focus on modern era
      GROUP BY b."playerID", FLOOR(b."yearID" / 10) * 10
    ),
    ranked_hr AS (
      SELECT 
        dh.*,
        p."namefirst" || ' ' || p."namelast" AS player_name,
        ROW_NUMBER() OVER (PARTITION BY dh.decade ORDER BY dh.total_hr DESC) as rank
      FROM decade_hr dh
      JOIN lahman."People" p ON dh."playerID" = p."playerid"
      WHERE dh.total_hr > 0
    )
    SELECT 
      decade,
      player_name,
      total_hr,
      rank
    FROM ranked_hr 
    WHERE rank <= 10
    ORDER BY decade, rank
    """

    return execute_query_with_validation(query)


def create_heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the data into a format suitable for heatmap visualization.

    Args:
        df: DataFrame with decade, player_name, total_hr, rank columns

    Returns:
        Pivot table with players as rows and decades as columns
    """
    # Create pivot table with players as rows and decades as columns
    heatmap_data = df.pivot(index="player_name", columns="decade", values="total_hr")

    # Fill NaN values with 0 for players who didn't have top 10 performance in certain decades
    heatmap_data = heatmap_data.fillna(0)

    # Sort by total home runs across all decades (descending)
    heatmap_data["total"] = heatmap_data.sum(axis=1)
    heatmap_data = heatmap_data.sort_values("total", ascending=False)
    heatmap_data = heatmap_data.drop("total", axis=1)

    return heatmap_data


def create_top_performers_heatmap(df: pd.DataFrame) -> None:
    """
    Create and save a heatmap visualization of top home run performers by decade.

    Args:
        df: DataFrame containing the home run data by decade
    """
    # Set up the plot style
    plt.style.use("default")
    sns.set_palette("viridis")

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(16, 12))

    # Create the heatmap
    heatmap = sns.heatmap(
        df,
        annot=True,  # Show values in cells
        fmt="g",  # Format numbers as integers
        cmap="YlOrRd",  # Color scheme from yellow to red
        cbar_kws={"label": "Home Runs"},
        linewidths=0.5,  # Add gridlines
        linecolor="white",
        ax=ax,
    )

    # Customize the plot
    ax.set_title(
        "Top 10 Home Run Hitters by Decade (1900-2020s)",
        fontsize=18,
        fontweight="bold",
        pad=20,
    )
    ax.set_xlabel("Decade", fontsize=14, fontweight="bold")
    ax.set_ylabel("Player", fontsize=14, fontweight="bold")

    # Format decade labels
    decade_labels = [f"{int(col)}s" for col in df.columns]
    ax.set_xticklabels(decade_labels, rotation=45, ha="right")

    # Adjust y-axis labels for better readability
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, ha="right")

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Save the plot
    output_path = "outputs/exercise_2_top_performers_heatmap.png"
    plt.savefig(
        output_path, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none"
    )

    print(f"Heatmap saved to: {output_path}")

    # Don't show the plot (headless mode)
    plt.close()


def print_data_summary(df: pd.DataFrame) -> None:
    """
    Print a summary of the data for validation.

    Args:
        df: DataFrame containing the home run data
    """
    print("Data Summary:")
    print(f"Total records: {len(df)}")
    print(f"Decades covered: {sorted(df['decade'].unique())}")
    print(f"Total unique players: {df['player_name'].nunique()}")
    print("\nTop 5 performers by total home runs:")

    # Calculate total home runs per player across all decades
    player_totals = (
        df.groupby("player_name")["total_hr"].sum().sort_values(ascending=False)
    )
    print(player_totals.head())


if __name__ == "__main__":
    print("Exercise 2: Creating Top Performers Heatmap")
    print("=" * 50)

    # Get the data from database
    print("Fetching top home run hitters by decade...")
    hr_data = get_top_hr_hitters_by_decade()

    # Print data summary
    print_data_summary(hr_data)

    # Transform data for heatmap
    print("\nTransforming data for heatmap visualization...")
    heatmap_data = create_heatmap_data(hr_data)

    print(
        f"Heatmap dimensions: {heatmap_data.shape[0]} players × {heatmap_data.shape[1]} decades"
    )

    # Create and save the heatmap
    print("Creating heatmap visualization...")
    create_top_performers_heatmap(heatmap_data)

    print("Exercise 2 completed successfully!")
