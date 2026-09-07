"""Main entry point for the e-commerce analysis pipeline."""

import logging

from ecommerce_analysis.logging_config import setup_logging
from ecommerce_analysis.data_loader import load_raw_data
from ecommerce_analysis.data_profiling import profile_data
from ecommerce_analysis.data_cleaning import clean_data
from ecommerce_analysis.analysis import (
    monthly_sales_trend,
    top_products,
    country_analysis,
    customer_analysis
)
from ecommerce_analysis.visualization import (
    plot_monthly_sales_trend,
    plot_top_products,
    plot_country_revenue,
    plot_customer_distribution,
    save_plot
)


def main() -> None:
    """Run the complete e-commerce data analysis pipeline."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("E-COMMERCE CUSTOMER BEHAVIOR ANALYSIS PIPELINE")
    logger.info("=" * 60)
    
    # Step 1: Load raw data
    logger.info("Step 1: Loading raw data...")
    df_raw = load_raw_data()
    logger.info(f"Loaded {df_raw.shape[0]:,} rows and {df_raw.shape[1]} columns")
    
    # Step 2: Profile raw data
    logger.info("\nStep 2: Profiling raw data...")
    profile = profile_data(df_raw)
    logger.info(f"Found {profile.duplicate_count:,} duplicate rows")
    logger.info(f"Found missing values in CustomerID: {profile.missing_values['CustomerID']:,}")
    logger.info(f"Found {profile.negative_prices:,} rows with negative prices")
    logger.info(f"Date range: {profile.date_range[0].date()} to {profile.date_range[1].date()}")
    
    # Step 3: Clean data
    logger.info("\nStep 3: Cleaning data...")
    df_cleaned = clean_data(df_raw)
    logger.info(f"Cleaned data: {df_cleaned.shape[0]:,} rows and {df_cleaned.shape[1]} columns")
    
    # Step 4: Analyze data
    logger.info("\nStep 4: Performing analysis...")
    
    # Monthly sales trend
    monthly_stats = monthly_sales_trend(df_cleaned)
    logger.info(f"Monthly stats generated for {len(monthly_stats)} months")
    
    # Top products
    top_10_products = top_products(df_cleaned, n=10)
    logger.info(f"Top product: {top_10_products.index[0]}")
    
    # Country analysis
    country_stats = country_analysis(df_cleaned)
    logger.info(f"Top country: {country_stats.index[0]}")
    
    # Customer analysis
    customer_stats = customer_analysis(df_cleaned)
    logger.info(f"Analyzed {len(customer_stats):,} unique customers")
    
    # Step 5: Create visualizations
    logger.info("\nStep 5: Creating visualizations...")
    
    # Monthly sales trend plot
    fig1 = plot_monthly_sales_trend(monthly_stats)
    save_plot(fig1, "monthly_sales_trend.png")
    plt.close(fig1)
    
    # Top products plot
    fig2 = plot_top_products(top_10_products)
    save_plot(fig2, "top_products.png")
    plt.close(fig2)
    
    # Country revenue plot
    fig3 = plot_country_revenue(country_stats)
    save_plot(fig3, "country_revenue.png")
    plt.close(fig3)
    
    # Customer distribution plot
    fig4 = plot_customer_distribution(customer_stats)
    save_plot(fig4, "customer_spending_distribution.png")
    plt.close(fig4)
    
    logger.info("\n" + "=" * 60)
    logger.info("ANALYSIS PIPELINE COMPLETED SUCCESSFULLY!")
    logger.info("=" * 60)
    
    # Print summary for user
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE - SUMMARY")
    print("=" * 60)
    print(f"Data: {df_cleaned.shape[0]:,} transactions analyzed")
    print(f"Time period: {df_cleaned['InvoiceDate'].min().date()} to {df_cleaned['InvoiceDate'].max().date()}")
    print(f"Top product: {top_10_products.index[0]} (£{top_10_products.iloc[0]['total_revenue']:,.2f})")
    print(f"Top country: {country_stats.index[0]} (£{country_stats.iloc[0]['total_revenue']:,.2f})")
    print(f"Unique customers: {len(customer_stats):,}")
    print(f"\nVisualizations saved to: reports/figures/")
    print("=" * 60)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    main()