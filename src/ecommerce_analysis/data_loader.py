"""Module for loading e-commerce data from various sources."""

import logging
import pandas as pd

from ecommerce_analysis import config

logger = logging.getLogger(__name__)


def load_raw_data() -> pd.DataFrame:
    """Load the raw e-commerce transaction data from Excel.
    
    Returns:
        pd.DataFrame: The raw transaction data with original values.
    """
    relative_path = config.RAW_DATA_FILE.relative_to(config.PROJECT_ROOT)
    logger.info(f"Loading raw data from {relative_path}")
    df = pd.read_excel(config.RAW_DATA_FILE)
    logger.info(f"{relative_path} was loaded successfully.")
    return df