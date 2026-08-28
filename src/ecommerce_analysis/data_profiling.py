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
