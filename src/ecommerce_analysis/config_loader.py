"""Module for loading and managing YAML configuration."""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from ecommerce_analysis import config

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Loads and manages YAML configuration for the analysis pipeline."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the configuration loader.
        
        Args:
            config_path: Path to YAML config file. Defaults to project root config.yaml.
        """
        if config_path is None:
            config_path = config.PROJECT_ROOT / "config.yaml"
        
        self.config_path = config_path
        self.config_data: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load and parse the YAML configuration file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config_data = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {self.config_path.relative_to(config.PROJECT_ROOT)}")
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML configuration: {e}")
            raise
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration value by section and key.
        
        Args:
            section: The configuration section (e.g., 'cleaning', 'analysis').
            key: The configuration key within the section.
            default: Default value if key not found.
            
        Returns:
            The configuration value, or default if not found.
        """
        try:
            return self.config_data[section][key]
        except (KeyError, TypeError):
            logger.warning(f"Config key '{section}.{key}' not found, using default: {default}")
            return default
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get an entire configuration section.
        
        Args:
            section: The configuration section name.
            
        Returns:
            Dictionary with all key-value pairs in the section.
        """
        return self.config_data.get(section, {})
    
    def validate(self) -> bool:
        """Validate that required configuration sections exist.
        
        Returns:
            True if all required sections are present.
        """
        required_sections = ['paths', 'cleaning', 'analysis', 'visualization', 'logging']
        
        for section in required_sections:
            if section not in self.config_data:
                logger.error(f"Missing required config section: {section}")
                return False
        
        logger.info("Configuration validation passed")
        return True


# Singleton instance for global access
_config_loader: Optional[ConfigLoader] = None


def get_config_loader() -> ConfigLoader:
    """Get or create the global configuration loader instance.
    
    Returns:
        ConfigLoader: The global configuration loader.
    """
    global _config_loader
    
    if _config_loader is None:
        _config_loader = ConfigLoader()
    
    return _config_loader