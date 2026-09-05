"""Main entry point for the e-commerce analysis pipeline."""

import logging

import pandas as pd

from ecommerce_analysis.logging_config import setup_logging
from ecommerce_analysis.data_loader import load_raw_data
from ecommerce_analysis.data_profiling import profile_data, show_profile
from ecommerce_analysis.data_cleaning import clean_data



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
    show_profile(profile)

    # cleaning data pipeline
    df_cleaned = clean_data(df)


if __name__ == "__main__":
    main()