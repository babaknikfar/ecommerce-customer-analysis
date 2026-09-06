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
    
    monthly_stats = df.groupby("YearMonth").agg(
        total_revenue=("TotalPrice", "sum"),
        transaction_count=("InvoiceNo", "nunique"),
        avg_order_value=("TotalPrice", "mean")
    ).round(2)
    
    logger.info(f"Generated monthly stats for {len(monthly_stats)} months")
    
    return monthly_stats