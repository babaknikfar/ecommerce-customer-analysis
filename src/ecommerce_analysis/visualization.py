"""Module for creating visualizations of e-commerce analysis results."""

import logging
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from ecommerce_analysis import config

logger = logging.getLogger(__name__)


def setup_plot_style() -> None:
    """Configure global matplotlib style for professional plots."""
    plt.style.use("seaborn-v0_8-darkgrid")
    sns.set_palette("husl")
    plt.rcParams["figure.figsize"] = (12, 6)
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["savefig.bbox"] = "tight"
    logger.info("Configured matplotlib style")


def save_plot(fig: plt.Figure, filename: str) -> Path:
    """Save a matplotlib figure to the figures directory.

    Args:
        fig: The matplotlib figure to save.
        filename: Name of the output file (with extension).

    Returns:
        Path: Path to the saved figure.
    """
    # Ensure figures directory exists
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # Save the figure
    filepath = config.FIGURES_DIR / filename
    fig.savefig(filepath)
    logger.info(f"Saved plot to {filepath.relative_to(config.PROJECT_ROOT)}")

    return filepath


def plot_monthly_sales_trend(monthly_stats: pd.DataFrame) -> plt.Figure:
    """Create a line plot of monthly sales trends.

    Args:
        monthly_stats: DataFrame from monthly_sales_trend() function.

    Returns:
        plt.Figure: Matplotlib figure with the plot.
    """
    setup_plot_style()

    fig, ax1 = plt.subplots()

    # Plot revenue on primary y-axis
    ax1.plot(
        monthly_stats.index.astype(str),
        monthly_stats["total_revenue"],
        marker="o",
        linewidth=2,
        color="blue",
        label="Total Revenue",
    )
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Total Revenue (£)")
    ax1.tick_params(axis="y")
    ax1.tick_params(axis="x", rotation=45)

    # Create secondary y-axis for transaction count
    ax2 = ax1.twinx()
    ax2.plot(
        monthly_stats.index.astype(str),
        monthly_stats["transaction_count"],
        marker="s",
        linewidth=2,
        color="orange",
        linestyle="--",
        label="Transactions",
    )
    ax2.set_ylabel("Number of Transactions")
    ax2.tick_params(axis="y")

    # Add legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.title("Monthly Sales Trend")
    plt.tight_layout()

    return fig


def plot_top_products(top_products: pd.DataFrame, top_n: int = 10) -> plt.Figure:
    """Create a horizontal bar plot of top products by revenue.

    Args:
        top_products: DataFrame from top_products() function.
        top_n: Number of top products to display.

    Returns:
        plt.Figure: Matplotlib figure with the plot.
    """
    setup_plot_style()

    # Sort and take top n
    products = top_products.head(top_n).sort_values("total_revenue")

    fig, ax = plt.subplots()
    bars = ax.barh(products.index, products["total_revenue"], color="steelblue")

    # Add value labels on bars
    for bar, value in zip(bars, products["total_revenue"]):
        ax.text(
            value,
            bar.get_y() + bar.get_height() / 2,
            f"£{value:,.0f}",
            ha="left",
            va="center",
        )

    ax.set_xlabel("Total Revenue (£)")
    ax.set_ylabel("Product")
    ax.set_title(f"Top {top_n} Products by Revenue")
    plt.tight_layout()

    return fig


def plot_country_revenue(country_stats: pd.DataFrame) -> plt.Figure:
    """Create a bar plot of revenue by country.

    Args:
        country_stats: DataFrame from country_analysis() function.

    Returns:
        plt.Figure: Matplotlib figure with the plot.
    """
    setup_plot_style()

    # Take top 10 countries
    countries = country_stats.head(10)

    fig, ax = plt.subplots()
    bars = ax.bar(countries.index, countries["total_revenue"], color="coral")

    # Add value labels
    for bar, value in zip(bars, countries["total_revenue"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"£{value:,.0f}",
            ha="center",
            va="bottom",
        )

    ax.set_xlabel("Country")
    ax.set_ylabel("Total Revenue (£)")
    ax.set_title("Revenue by Country (Top 10)")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()

    return fig


def plot_customer_distribution(customer_stats: pd.DataFrame) -> plt.Figure:
    """Create a histogram of customer spending distribution.

    Args:
        customer_stats: DataFrame from customer_analysis() function.

    Returns:
        plt.Figure: Matplotlib figure with the plot.
    """
    setup_plot_style()

    fig, ax = plt.subplots()

    # Plot histogram with log scale (customer spending is often skewed)
    ax.hist(customer_stats["total_spent"], bins=50, color="green", alpha=0.7)
    ax.set_xlabel("Total Spent (£)")
    ax.set_ylabel("Number of Customers")
    ax.set_title("Distribution of Customer Spending")
    ax.set_yscale("log")  # Log scale for better visualization of skewed data

    plt.tight_layout()

    return fig
