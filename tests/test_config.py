"""Tests for the configuration module."""

from pathlib import Path

from ecommerce_analysis import config

def test_project_root_exists():
    """Test that the project root directory exists."""
    assert config.PROJECT_ROOT.exists()
    assert config.PROJECT_ROOT.is_dir()

def test_raw_data_file_exists():
    """Test that the raw data file exists."""
    assert config.RAW_DATA_FILE.exists()
    assert config.RAW_DATA_FILE.is_file()

def test_paths_are_path_objects():
    """Test that all paths are pathlib.Path objects."""
    assert isinstance(config.PROJECT_ROOT, Path)
    assert isinstance(config.DATA_DIR, Path)
    assert isinstance(config.RAW_DATA_FILE, Path)
    assert isinstance(config.PROCESSED_DATA_DIR, Path)
    assert isinstance(config.REPORTS_DIR, Path)
    assert isinstance(config.FIGURES_DIR, Path)

def test_seed_value():
    """Test that the random seed is set to 42 for reproducibility."""
    assert config.SEED == 42
    assert isinstance(config.SEED, int)

def test_path_structure():
    """Test that data directory structure is correctly nested."""
    assert config.RAW_DATA_DIR.parent == config.DATA_DIR
    assert config.PROCESSED_DATA_DIR.parent == config.DATA_DIR
    assert config.DATA_DIR.parent == config.PROJECT_ROOT
    assert config.FIGURES_DIR.parent == config.REPORTS_DIR
    assert config.REPORTS_DIR.parent == config.PROJECT_ROOT