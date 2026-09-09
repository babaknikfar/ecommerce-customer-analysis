"""Configuration settings for the e-commerce analysis project.

This module provides:
- Path constants (derived from project structure)
- YAML configuration access
- Backward-compatible constants for existing code
"""

from pathlib import Path
from typing import Final, Any, Dict

from ecommerce_analysis.config_loader import get_config_loader

# ============================================
# Path Constants (derived from project structure)
# ============================================
PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent.parent
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
RAW_DATA_DIR: Final[Path] = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Final[Path] = DATA_DIR / "processed"
REPORTS_DIR: Final[Path] = PROJECT_ROOT / "reports"
FIGURES_DIR: Final[Path] = REPORTS_DIR / "figures"

# ============================================
# File Constants
# ============================================
RAW_DATA_FILE: Final[Path] = RAW_DATA_DIR / "online_retail.xlsx"
CONFIG_FILE: Final[Path] = PROJECT_ROOT / "config.yaml"

# ============================================
# Analysis Settings
# ============================================
SEED: Final[int] = 42  # Random seed for reproducibility

# ============================================
# YAML Configuration Access
# ============================================
def get_config(section: str, key: str, default: Any = None) -> Any:
    """Get a configuration value from the YAML config file.
    
    Args:
        section: Configuration section name.
        key: Configuration key within the section.
        default: Default value if not found.
        
    Returns:
        The configuration value.
    """
    loader = get_config_loader()
    return loader.get(section, key, default)


def get_cleaning_config() -> Dict[str, Any]:
    """Get the complete cleaning configuration section.
    
    Returns:
        Dictionary with all cleaning settings.
    """
    loader = get_config_loader()
    return loader.get_section('cleaning')


def get_analysis_config() -> Dict[str, Any]:
    """Get the complete analysis configuration section.
    
    Returns:
        Dictionary with all analysis settings.
    """
    loader = get_config_loader()
    return loader.get_section('analysis')


def get_visualization_config() -> Dict[str, Any]:
    """Get the complete visualization configuration section.
    
    Returns:
        Dictionary with all visualization settings.
    """
    loader = get_config_loader()
    return loader.get_section('visualization')


def get_logging_config() -> Dict[str, Any]:
    """Get the complete logging configuration section.
    
    Returns:
        Dictionary with all logging settings.
    """
    loader = get_config_loader()
    return loader.get_section('logging')