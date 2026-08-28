"""Main entry point for the e-commerce analysis pipeline."""

import logging

import pandas as pd

from ecommerce_analysis.logging_config import setup_logging
from ecommerce_analysis.data_loader import load_raw_data
from ecommerce_analysis.data_profiling import profile_data


def main() -> None:
    """Run the data profiling pipeline."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting e-commerce data analysis pipeline")
    
    # Loading the raw data
    logger.info("Loading raw data...")
    df = load_raw_data()
    
    # Data profiling
    logger.info("Profiling data...")
    profile = profile_data(df)
    
    # Readable output
    print("\n" + "="*60)
    print("E-COMMERCE DATA PROFILE SUMMARY")
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
        "missing_pct": [f"{count/len(df):.1%}" for count in profile.missing_values.values()],
        "unique": [f"{count:,}" for count in profile.unique_counts.values()],
    }, index=profile.columns)
    
    print(column_info.to_string())
    print("="*60)


if __name__ == "__main__":
    main()