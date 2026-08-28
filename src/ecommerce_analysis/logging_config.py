"""Logging configuration for the e-commerce analysis package."""

import logging
import sys
from typing import Optional
from pathlib import Path


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels."""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[1;31m'  # Bold Red
    }
    # Colors for other components
    TIME_COLOR = '\033[38;5;208m'    # Orange
    MODULE_COLOR = '\033[35m'        # Magenta/Purple
    MESSAGE_COLOR = '\033[37m'       # White/Gray
    RESET = '\033[0m'
    
    def format(self, record):
        # Color the level name
        level_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{level_color}{record.levelname}{self.RESET}"
        # Color the module name
        record.name = f"{self.MODULE_COLOR}{record.name}{self.RESET}"
        # Color the message
        record.msg = f"{self.MESSAGE_COLOR}{record.msg}{self.RESET}"
        # Format with custom date color
        original_format = self._style._fmt
        self._style._fmt = original_format.replace(
            '%(asctime)s',
            f'{self.TIME_COLOR}%(asctime)s{self.RESET}'
        )
        result = super().format(record)
        # Restore original format
        self._style._fmt = original_format
        return result


def setup_logging(level: int = logging.INFO, log_file: Optional[Path] = None) -> None:
    """Configure logging for the entire package.
    
    Args:
        level: The logging level (default: logging.INFO)
        log_file: Optional path to a log file. If None, logs only to console.
    """

    # Create formatter
    formatter = ColoredFormatter(
        fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()  # Prevent duplicate handlers
    root_logger.addHandler(console_handler)

    # Add file handler if log_file is provided
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)