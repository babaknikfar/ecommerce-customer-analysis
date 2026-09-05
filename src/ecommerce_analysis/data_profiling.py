"""Module for profiling and analyzing data quality issues."""

import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple

import pandas as pd

from ecommerce_analysis import config

logger = logging.getLogger(__name__)


@dataclass
class DataProfile:
    """Container for data profiling results."""
    shape: Tuple[int, int]
    columns: List[str]
    dtypes: Dict[str, str]
    missing_values: Dict[str, int]
    duplicate_count: int
    negative_quantities: int
    negative_prices: int
    zero_quantities: int
    zero_prices: int
    date_range: Tuple[pd.Timestamp, pd.Timestamp]
    unique_counts: Dict[str, int]

def profile_data(df: pd.DataFrame) -> DataProfile:
    """Generate a comprehensive profile of the dataset.
    
    Args:
        df: The DataFrame to profile.
        
    Returns:
        DataProfile: Container with all profiling results.
    """

    relative_path = config.RAW_DATA_FILE.relative_to(config.PROJECT_ROOT)
    logger.info(f"Profiling {relative_path}")

    return DataProfile(
        shape=df.shape,
        columns=df.columns.to_list(),
        dtypes={col: str(dtype) for col, dtype in df.dtypes.items()},
        missing_values=df.isnull().sum().to_dict(),
        duplicate_count=df.duplicated().sum(),
        negative_quantities=len(df[df["Quantity"] < 0]),
        negative_prices=len(df[df["UnitPrice"] < 0]),
        zero_quantities=len(df[df["Quantity"] == 0]),
        zero_prices=len(df[df["UnitPrice"] == 0]),
        date_range=(df["InvoiceDate"].min(), df["InvoiceDate"].max()),
        unique_counts=df.nunique().to_dict(),
    )

def show_profile(profile: DataProfile) -> None:
    """Human readable presentation of the data profile."""
    print("\n" + "="*60)
    print("DATA PROFILE SUMMARY")
    print("="*60)
    
    print(f"\nDataset Shape: {profile.shape[0]:,} rows and {profile.shape[1]} columns")
    print(f"Duplicate Rows: {profile.duplicate_count:,}")
    print(f"Date Range: {profile.date_range[0].strftime('%Y-%m-%d')} to {profile.date_range[1].strftime('%Y-%m-%d')}")
    
    print(f"\nData Quality Issues:")
    print(f"  - Negative Quantities: {profile.negative_quantities:,}")
    print(f"  - Negative Prices: {profile.negative_prices:,}")
    print(f"  - Zero Quantities: {profile.zero_quantities:,}")
    print(f"  - Zero Prices: {profile.zero_prices:,}")
        
    # Column information
    print(f"\nColumn Details:")
    column_info = pd.DataFrame({
        "dtype": [str(dtype) for dtype in profile.dtypes.values()],
        "missing": [f"{count:,}" for count in profile.missing_values.values()],
        "missing_pct": [f"{count/profile.shape[0]:.1%}" for count in profile.missing_values.values()],
        "unique": [f"{count:,}" for count in profile.unique_counts.values()],
    }, index=profile.columns)
    
    print(column_info.to_string())
    print("="*60)