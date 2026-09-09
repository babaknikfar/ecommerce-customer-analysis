"""Module for analyzing e-commerce transaction data."""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly sales metrics.

    Args:
        df: Cleaned DataFrame with TotalPrice and YearMonth columns.

    Returns:
        pd.DataFrame: Monthly aggregated sales data with columns:
            - total_revenue: Sum of TotalPrice
            - transaction_count: Number of unique invoices
            - avg_order_value: Average revenue per transaction
    """
    logger.info("Calculating monthly sales trends...")

    monthly_stats = (
        df.groupby("YearMonth")
        .agg(
            total_revenue=("TotalPrice", "sum"),
            transaction_count=("InvoiceNo", "nunique"),
            avg_order_value=("TotalPrice", "mean"),
        )
        .round(2)
    )

    logger.info(f"Generated monthly stats for {len(monthly_stats)} months")

    return monthly_stats


def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Identify top products by revenue and quantity.

    Args:
        df: Cleaned DataFrame with TotalPrice and Description columns.
        n: Number of top products to return (default: 10).

    Returns:
        pd.DataFrame: Top n products with revenue, quantity, and transaction count.
    """
    logger.info(f"Identifying top {n} products...")

    product_stats = (
        df.groupby("Description")
        .agg(
            total_revenue=("TotalPrice", "sum"),
            total_quantity=("Quantity", "sum"),
            transaction_count=("InvoiceNo", "nunique"),
            avg_unit_price=("UnitPrice", "mean"),
        )
        .round(2)
    )

    # Sort by revenue descending and take top n
    top_products = product_stats.sort_values("total_revenue", ascending=False).head(n)

    logger.info(
        f"Top product: {top_products.index[0]} with revenue {top_products.iloc[0]['total_revenue']:,.2f}"
    )

    return top_products


def country_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze sales performance by country.

    Args:
        df: Cleaned DataFrame with Country and TotalPrice columns.

    Returns:
        pd.DataFrame: Country-level sales metrics sorted by revenue.
    """
    logger.info("Analyzing sales by country...")

    country_stats = (
        df.groupby("Country")
        .agg(
            total_revenue=("TotalPrice", "sum"),
            transaction_count=("InvoiceNo", "nunique"),
            unique_customers=("CustomerID", "nunique"),
            avg_order_value=("TotalPrice", "mean"),
        )
        .round(2)
    )

    # Calculate revenue share percentage
    country_stats["revenue_share_pct"] = (
        country_stats["total_revenue"] / country_stats["total_revenue"].sum() * 100
    ).round(2)

    # Sort by revenue descending
    country_stats = country_stats.sort_values("total_revenue", ascending=False)

    logger.info(
        f"Top country: {country_stats.index[0]} with {country_stats.iloc[0]['revenue_share_pct']:.1f}% of revenue"
    )

    return country_stats


def customer_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze customer purchasing behavior.

    Args:
        df: Cleaned DataFrame with CustomerID and TotalPrice columns.

    Returns:
        pd.DataFrame: Customer-level metrics for top customers.
    """
    logger.info("Analyzing customer purchasing behavior...")

    customer_stats = df.groupby("CustomerID").agg(
        total_spent=("TotalPrice", "sum"),
        transaction_count=("InvoiceNo", "nunique"),
        total_items=("Quantity", "sum"),
        first_purchase=("InvoiceDate", "min"),
        last_purchase=("InvoiceDate", "max"),
    )

    # Calculate customer lifetime (days between first and last purchase)
    customer_stats["customer_lifetime_days"] = (
        customer_stats["last_purchase"] - customer_stats["first_purchase"]
    ).dt.days

    # Calculate average order value per customer
    customer_stats["avg_order_value"] = (
        customer_stats["total_spent"] / customer_stats["transaction_count"]
    ).round(2)

    # Sort by total spent descending
    customer_stats = customer_stats.sort_values("total_spent", ascending=False)

    logger.info(f"Analyzed {len(customer_stats):,} unique customers")

    return customer_stats
