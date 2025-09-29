"""
Exercise 0: Total Home Runs by Year (2010-2024)
Creates a bar plot showing league-wide home run production trends.
"""

from dotenv import load_dotenv

load_dotenv()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from mlb.db import execute_query_with_validation


def fetch_home_run_data() -> pd.DataFrame:
    """
    Fetch total home runs by year from the database.

    Returns:
        DataFrame with yearID and total_home_runs columns
    """
    query = """
    SELECT "yearID", 
           SUM(CAST("HR" AS INTEGER)) as total_home_runs
    FROM lahman."Batting" 
    WHERE "yearID" >= 2010 AND "yearID" <= 2024
      AND "HR" IS NOT NULL
      AND "HR" != ''
    GROUP BY "yearID"
    ORDER BY "yearID"
    """

    df = execute_query_with_validation(query)
    return df


def create_visualization(df: pd.DataFrame, output_path: str) -> None:
    """
    Create a bar plot of total home runs by year.

    Args:
        df: DataFrame with yearID and total_home_runs
        output_path: Path to save the plot
    """
    # Set style for professional appearance
    sns.set_style("whitegrid")
    plt.figure(figsize=(14, 8))

    # Create color palette - gradient from light to dark blue
    colors = sns.color_palette("Blues_r", n_colors=len(df))

    # Create bar plot
    bars = plt.bar(
        df["yearID"],
        df["total_home_runs"],
        color=colors,
        edgecolor="black",
        linewidth=1.2,
    )

    # Customize the plot
    plt.title(
        "Total Home Runs in Major League Baseball by Year (2010-2024)",
        fontsize=18,
        fontweight="bold",
        pad=20,
    )
    plt.xlabel("Year", fontsize=14, fontweight="bold")
    plt.ylabel("Total Home Runs", fontsize=14, fontweight="bold")

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{int(height):,}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    # Format y-axis with comma separators
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{int(x):,}"))

    # Set x-axis ticks to show all years
    plt.xticks(df["yearID"], rotation=45, ha="right")

    # Add grid for better readability
    plt.grid(axis="y", alpha=0.3, linestyle="--")

    # Tight layout to prevent label cutoff
    plt.tight_layout()

    # Save the figure
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Plot saved to: {output_path}")

    # Close the figure to free memory
    plt.close()


def validate_output(output_path: str) -> None:
    """
    Validate that the output file was created successfully.

    Args:
        output_path: Path to the output file
    """
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"✓ Output file created successfully: {output_path}")
        print(f"✓ File size: {file_size:,} bytes")
    else:
        print(f"✗ ERROR: Output file not found: {output_path}")


def main() -> None:
    """Main execution function."""
    print("Exercise 0: Total Home Runs by Year")
    print("=" * 50)

    # Fetch data from database
    print("\n1. Fetching home run data from database...")
    df = fetch_home_run_data()
    print(f"✓ Retrieved {len(df)} years of data")
    print(f"\nData summary:")
    print(df.to_string(index=False))

    # Create visualization
    print("\n2. Creating visualization...")
    output_path = "outputs/exercise_0/total_home_runs_by_year.png"
    create_visualization(df, output_path)

    # Validate output
    print("\n3. Validating output...")
    validate_output(output_path)

    print("\n" + "=" * 50)
    print("Exercise 0 complete!")


if __name__ == "__main__":
    main()
