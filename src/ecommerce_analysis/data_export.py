"""Module for exporting cleaned data and analysis results."""

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

from ecommerce_analysis import config

logger = logging.getLogger(__name__)


def export_to_csv(
    df: pd.DataFrame,
    filename: str,
    directory: Optional[Path] = None
) -> Path:
    """Export a DataFrame to CSV format.
    
    Args:
        df: DataFrame to export.
        filename: Name of the output file (with .csv extension).
        directory: Directory to save to. Defaults to processed data directory.
        
    Returns:
        Path: Path to the saved file.
    """
    if directory is None:
        directory = config.PROCESSED_DATA_DIR
    
    # Ensure directory exists
    directory.mkdir(parents=True, exist_ok=True)
    
    # Save the file
    filepath = directory / filename
    df.to_csv(filepath, index=False)
    
    logger.info(f"Exported {len(df):,} rows to {filepath.relative_to(config.PROJECT_ROOT)}")
    
    return filepath


def export_to_excel(
    dfs: dict[str, pd.DataFrame],
    filename: str,
    directory: Optional[Path] = None
) -> Path:
    """Export multiple DataFrames to a single Excel file with multiple sheets.
    
    Args:
        dfs: Dictionary of sheet names and DataFrames.
        filename: Name of the output file (with .xlsx extension).
        directory: Directory to save to. Defaults to reports directory.
        
    Returns:
        Path: Path to the saved file.
    """
    if directory is None:
        directory = config.REPORTS_DIR
    
    # Ensure directory exists
    directory.mkdir(parents=True, exist_ok=True)
    
    # Save to Excel with multiple sheets
    filepath = directory / filename
    
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            logger.info(f"Added sheet '{sheet_name}' with {len(df):,} rows")
    
    logger.info(f"Exported Excel file to {filepath.relative_to(config.PROJECT_ROOT)}")
    
    return filepath


def export_analysis_results(
    monthly_stats: pd.DataFrame,
    top_products: pd.DataFrame,
    country_stats: pd.DataFrame,
    customer_stats: pd.DataFrame,
    cleaned_df: pd.DataFrame
) -> dict[str, Path]:
    """Export all analysis results to various formats.
    
    Args:
        monthly_stats: Monthly sales statistics.
        top_products: Top products analysis.
        country_stats: Country-wise statistics.
        customer_stats: Customer analysis results.
        cleaned_df: Complete cleaned dataset.
        
    Returns:
        Dictionary of exported file paths.
    """
    logger.info("Starting data export...")
    
    exported_files = {}
    
    # Export cleaned data
    cleaned_path = export_to_csv(
        cleaned_df,
        "cleaned_transactions.csv"
    )
    exported_files['cleaned_data'] = cleaned_path
    
    # Export analysis results to Excel
    excel_path = export_to_excel(
        {
            'Monthly Sales': monthly_stats,
            'Top Products': top_products,
            'Country Analysis': country_stats,
            'Customer Analysis': customer_stats.head(1000)  # Limit to first 1000 customers
        },
        "analysis_results.xlsx"
    )
    exported_files['analysis_excel'] = excel_path
    
    # Export individual CSVs for easy access
    monthly_path = export_to_csv(
        monthly_stats,
        "monthly_sales.csv",
        directory=config.REPORTS_DIR
    )
    exported_files['monthly_stats'] = monthly_path
    
    country_path = export_to_csv(
        country_stats,
        "country_analysis.csv",
        directory=config.REPORTS_DIR
    )
    exported_files['country_stats'] = country_path
    
    logger.info(f"Data export complete. Exported {len(exported_files)} files.")
    
    return exported_files


def export_summary_report(
    df: pd.DataFrame,
    filename: str = "summary_report.txt"
) -> Path:
    """Export a text summary of the dataset.
    
    Args:
        df: Cleaned DataFrame to summarize.
        filename: Name of the output file.
        
    Returns:
        Path: Path to the saved report.
    """
    report_path = config.REPORTS_DIR / filename
    config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("E-COMMERCE DATA ANALYSIS SUMMARY\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Data Period: {df['InvoiceDate'].min().date()} to {df['InvoiceDate'].max().date()}\n")
        f.write(f"Total Transactions: {len(df):,}\n")
        f.write(f"Unique Customers: {df['CustomerID'].nunique():,}\n")
        f.write(f"Unique Products: {df['StockCode'].nunique():,}\n")
        f.write(f"Countries Served: {df['Country'].nunique():,}\n\n")
        
        f.write(f"Total Revenue: £{df['TotalPrice'].sum():,.2f}\n")
        f.write(f"Average Order Value: £{df['TotalPrice'].mean():.2f}\n")
        f.write(f"Total Items Sold: {df[df['Quantity'] > 0]['Quantity'].sum():,}\n\n")
        
        f.write("Top 5 Countries by Revenue:\n")
        top_countries = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(5)
        for country, revenue in top_countries.items():
            f.write(f"  {country}: £{revenue:,.2f}\n")
        
        f.write("\n" + "=" * 60 + "\n")
    
    logger.info(f"Exported summary report to {report_path.relative_to(config.PROJECT_ROOT)}")
    
    return report_path