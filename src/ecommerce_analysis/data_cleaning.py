"""Module for cleaning and preprocessing e-commerce transaction data."""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows from the dataset.
    
    Args:
        df: The DataFrame to clean.
        
    Returns:
        pd.DataFrame: DataFrame with duplicates removed.
    """

    # Count duplicate rows
    duplicate_count = df.duplicated().sum()

    # drop duplicates
    df_cleaned = df.drop_duplicates()

    # log the operation
    logger.info(f"Removed {duplicate_count} duplicate rows.")

    return df_cleaned


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values in the dataset.
    
    Strategy:
    - Drop rows with missing CustomerID (can't be used for customer analysis)
    - Fill missing Description with 'Unknown' (preserves transaction data)
    
    Args:
        df: The DataFrame to clean.
        
    Returns:
        pd.DataFrame: DataFrame with missing values handled.
    """
    # Count missing values before cleaning
    missing_before = df.isna().sum()
    logger.info(f"Missing values before cleaning:\n{missing_before}")
    
    # Drop rows where CustomerID is missing
    df_cleaned = df.dropna(subset=['CustomerID']).copy()
    
    # Fill missing Description with 'Unknown'
    df_cleaned.loc[:, 'Description'] = df_cleaned['Description'].fillna('Unknown')
    
    # Log the cleaning operations
    dropped_rows = len(df) - len(df_cleaned)
    logger.info(f"Dropped {dropped_rows:,} rows with missing CustomerID")
    logger.info(f"Filled missing Description values with 'Unknown'")
    
    # Count missing values after cleaning
    missing_after = df_cleaned.isna().sum()
    logger.info(f"Missing values after cleaning:\n{missing_after}")
    
    return df_cleaned


def remove_invalid_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Remove transactions with invalid prices or quantities.
    
    Strategy:
    - Remove rows with negative UnitPrice (data entry errors)
    - Remove rows with zero UnitPrice (free items or errors)
    - Remove rows with zero Quantity (no items purchased)
    - Keep negative Quantity (represents returns/cancellations)
    
    Args:
        df: The DataFrame to clean.
        
    Returns:
        pd.DataFrame: DataFrame with invalid transactions removed.
    """
    # Count invalid transactions before removal
    negative_prices = (df['UnitPrice'] < 0).sum()
    zero_prices = (df['UnitPrice'] == 0).sum()
    zero_quantities = (df['Quantity'] == 0).sum()
    
    logger.info(f"Found {negative_prices:,} rows with negative prices")
    logger.info(f"Found {zero_prices:,} rows with zero prices")
    logger.info(f"Found {zero_quantities:,} rows with zero quantities")
    
    # Remove invalid transactions
    df_cleaned = df[
        (df['UnitPrice'] > 0) &      # Keep only positive prices
        (df['Quantity'] != 0)        # Keep only non-zero quantities
    ].copy()
    
    # Log the result
    removed_rows = len(df) - len(df_cleaned)
    logger.info(f"Removed {removed_rows:,} invalid transactions")
    logger.info(f"Remaining transactions: {len(df_cleaned):,}")
    
    return df_cleaned


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived features to the dataset.
    
    Adds:
    - TotalPrice: Quantity * UnitPrice (transaction value)
    - YearMonth: InvoiceDate truncated to month (for time-series analysis)
    
    Args:
        df: The DataFrame to enhance.
        
    Returns:
        pd.DataFrame: DataFrame with new features added.
    """
    # Create a copy to avoid modifying the original
    df_enhanced = df.copy()
    
    # Add TotalPrice feature
    df_enhanced['TotalPrice'] = df_enhanced['Quantity'] * df_enhanced['UnitPrice']
    logger.info(f"Added TotalPrice column (Quantity * UnitPrice)")
    
    # Add YearMonth feature for time-series analysis
    df_enhanced['YearMonth'] = df_enhanced['InvoiceDate'].dt.to_period('M')
    logger.info(f"Added YearMonth column for monthly aggregation")
    
    # Log summary statistics of new features
    logger.info(f"TotalPrice stats: min={df_enhanced['TotalPrice'].min():.2f}, "
                f"max={df_enhanced['TotalPrice'].max():.2f}, "
                f"mean={df_enhanced['TotalPrice'].mean():.2f}")
    
    return df_enhanced


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Execute the complete data cleaning pipeline.
    
    Pipeline steps:
    1. Remove duplicate rows
    2. Handle missing values (drop missing CustomerID, fill Description)
    3. Remove invalid transactions (negative/zero prices, zero quantities)
    4. Add derived features (TotalPrice, YearMonth)
    
    Args:
        df: The raw DataFrame to clean.
        
    Returns:
        pd.DataFrame: Fully cleaned and enhanced DataFrame.
    """
    logger.info("Starting data cleaning pipeline...")
    logger.info(f"Initial shape: {df.shape[0]:,} rows, {df.shape[1]} columns")
    
    # Step 1: Remove duplicates
    df = remove_duplicates(df)
    logger.info(f"After removing duplicates: {df.shape[0]:,} rows")
    
    # Step 2: Handle missing values
    df = handle_missing_values(df)
    logger.info(f"After handling missing values: {df.shape[0]:,} rows")
    
    # Step 3: Remove invalid transactions
    df = remove_invalid_transactions(df)
    logger.info(f"After removing invalid transactions: {df.shape[0]:,} rows")
    
    # Step 4: Add derived features
    df = add_features(df)
    logger.info(f"After adding features: {df.shape[0]:,} rows, {df.shape[1]} columns")
    
    logger.info("Data cleaning pipeline completed successfully!")
    
    return df