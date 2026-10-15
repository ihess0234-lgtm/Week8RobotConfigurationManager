# from test_configuration import TestConfigurationManagerLoad, TestConfigurationManagerGet, TestConfigurationManagerValidate
from typing import Any, Optional
import json, logging, os, yaml

# reads file
# with open('robot_config.json', 'r') as file:
#     config = json.load(file)

# # Writing configuration files (creates or overwrites)
# with open('robot_config.json', 'w') as file:
#     json.dump(config, file, indent=2)

# # Appending sensor logs
# with open('sensor_log.txt', 'a') as file:
#     file.write(f"[test1] test2\n")

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class ConfigurationError(Exception):
    """Base exception for all configuration errors."""
    pass

class ConfigFileNotFoundError(ConfigurationError):
    """Raised when the configuration file cannot be found."""
    def __init__(self, file_path: str):
        self.file_path = file_path
        super().__init__(f"Configuration file not found: {file_path}")

class ConfigParseError(ConfigurationError):
    """Raised when a file exists but cannot be parsed."""
    def __init__(self, file_path: str, reason: str):
        self.file_path = file_path
        super().__init__(f"Failed to parse '{file_path}': {reason}")

class ConfigValidationError(ConfigurationError):
    """Raised when configuration data fails validation."""
    def __init__(self, errors: list):
        self.errors = errors
        details = "\n  - ".join(errors)
        super().__init__(f"Configuration validation failed:\n  - {details}")


class ConfigurationManager():

    """Manages robot configurations from files."""

    def __init__(self, config_file):
        """Initialize with configuration file path."""
        self.config_file = config_file
        self.config: dict[str, Any] = {}
        logger.debug("ConfigurationManager initialised with: %s", config_file)
        self.load()

    def load(self):
        """Load configuration from file (auto-detect format)."""
        if not os.path.exists(self.config_file):
            logger.error("Config file not found: %s", self.config_file)
            raise ConfigFileNotFoundError(self.config_file)

        file_format = self._detect_format(self.config_file)
        # Determine format from file extension
        # Parse appropriate format
        # Store in self.config

    def get(self, key, default=None):
        """Safely retrieve configuration value.

        Supports dot notation: get('sensors.ir_count')
        Returns default if key not found.
        """

    def save(self, output_file=None):
        """Save current configuration to file."""
        # Save to file (auto-detect format from extension)

    def validate(self) -> None:
        """Validate configuration data.

        Raises:
            ConfigValidationError: If any validation checks fail.
        """
        """Validate calibration data — same pattern you will apply to ConfigurationManager."""
        # errors = []

        # # Check required fields exist
        # if 'sensor_name' not in self.data:
        #     errors.append("Missing required field: sensor_name")

        # # Check data types
        # if 'channels' in self.data:
        #     if not isinstance(self.data['channels'], int):
        #         errors.append("channels must be integer")
        #     elif self.data['channels'] <= 0:
        #         errors.append("channels must be greater than zero")

        # # Raise with all errors at once — don't stop at the first failure
        # if errors:
        #     raise CalibrationValidationError(errors)
        
        # Check required fields exist
        # Check data types are correct
        # Check values are in valid ranges
        # Raise ConfigValidationError with all errors if any fail

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    sample = ConfigurationManager('example_configs/line_follower.yaml')
    sample.validate()
    print(sample.get('robot_id'))

try:
    config_mgr = ConfigurationManager('json_robot_config.json')
    config_mgr.validate()
except ConfigFileNotFoundError as e:
    logger.warning("No config file — using defaults. (%s)", e.file_path)
    config_mgr = ConfigurationManager.from_defaults()
except ConfigParseError as e:
    logger.error("Corrupted config file: %s", e)
    raise  # Surface this — don't silently swallow it
except ConfigValidationError as e:
    logger.error("Invalid config: %s", e)
    raise

config_mgr = ConfigurationManager('json_robot_config.json')
robot_name = config_mgr.get('name')
ir_count = config_mgr.get('sensors.ir_count', default=4)

config_mgr.validate()  # Raises ConfigValidationError if invalid
print("Configuration is valid")


# Loads JSON and one other format (XML or YAML — your choice)
# Auto-detect format from file extension
# Raise your ConfigFileNotFoundError when file is missing
# Raise your ConfigParseError for corrupted or invalid files

# Supports value access

# Simple keys: get('robot_id')
# Nested keys with dot notation: get('sensors.ir_count')
# Default values: get('unknown_key', default=0)

# Validates configuration

# Required fields check
# Type validation
# Range validation (e.g., sensor count > 0)
# Raises your ConfigValidationError listing all failures

# Saves configuration

# Write back to file in detected format
# Pretty-printed for readability