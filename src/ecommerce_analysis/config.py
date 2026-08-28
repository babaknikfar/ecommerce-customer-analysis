"""Configuration settings for the e-commerce analysis project."""

from pathlib import Path
from typing import Final

# Paths
PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent.parent
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
RAW_DATA_DIR: Final[Path] = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Final[Path] = DATA_DIR / "processed"
REPORTS_DIR: Final[Path] = PROJECT_ROOT / "reports"
FIGURES_DIR: Final[Path] = REPORTS_DIR / "figures"

# Files
RAW_DATA_FILE: Final[Path] = RAW_DATA_DIR / "online_retail.xlsx"

# Analysis settings
SEED: Final[int] = 42  # Random seed for reproducibility