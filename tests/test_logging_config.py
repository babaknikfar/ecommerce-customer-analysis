"""Tests for the logging configuration module."""

import logging
from pathlib import Path

from ecommerce_analysis.logging_config import setup_logging


def test_setup_logging_creates_file(tmp_path: Path):
    """Test that file logging creates a log file."""
    log_file = tmp_path / "test.log"
    setup_logging(log_file=log_file)
    
    # Log a test message
    logging.info("Test log message")
    content = log_file.read_text()
    
    # Assert file exists and contains message
    assert log_file.exists()
    assert "Test log message" in content


def test_setup_logging_prevents_duplicate_handlers():
    """Test that calling setup_logging multiple times doesn't duplicate handlers."""
    setup_logging()
    initial_count = len(logging.getLogger().handlers)
    
    setup_logging()
    final_count = len(logging.getLogger().handlers)
    
    assert initial_count == final_count


