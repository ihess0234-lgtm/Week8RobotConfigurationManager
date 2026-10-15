# from test_configuration import TestConfigurationManagerLoad, TestConfigurationManagerGet, TestConfigurationManagerValidate
import json, logging, os

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
        super().__init__(f"Validation failed: {'; '.join(errors)}")

class CalibrationError(Exception):
    """Base exception for all calibration errors.

    All CalibrationReader exceptions inherit from this,
    allowing callers to catch broadly or specifically.
    """
    pass


class CalibrationFileNotFoundError(CalibrationError):
    """Raised when the calibration file cannot be found.

    Args:
        file_path: The path that was searched.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        super().__init__(f"Calibration file not found: {file_path}")


class CalibrationParseError(CalibrationError):
    """Raised when a calibration file exists but cannot be parsed.

    Args:
        file_path: The file that failed to parse.
        reason: Human-readable description of the parse failure.
    """
    def __init__(self, file_path: str, reason: str):
        self.file_path = file_path
        self.reason = reason
        super().__init__(f"Failed to parse '{file_path}': {reason}")


class CalibrationValidationError(CalibrationError):
    """Raised when calibration data fails validation checks.

    Args:
        errors: List of validation error messages.
    """
    def __init__(self, errors: list):
        self.errors = errors
        error_list = "\n  - ".join(errors)
        super().__init__(f"Calibration validation failed:\n  - {error_list}")

# try:
#     cal = CalibrationReader('ir_sensor_cal.json')
#     cal.validate()
# except CalibrationError as e:
#     logger.error("Calibration problem: %s", e)

# # OR catch specific problems to handle differently
# try:
#     cal = CalibrationReader('ir_sensor_cal.json')
#     cal.validate()
# except CalibrationFileNotFoundError:
#     cal = CalibrationReader.from_defaults()         # Fallback to defaults
# except CalibrationParseError as e:
#     logger.error("Corrupted calibration file: %s", e.file_path)
#     raise                                           # Re-raise — needs attention
# except CalibrationValidationError as e:
#     for error in e.errors:
#         logger.warning("Calibration issue: %s", error)


logger = logging.getLogger(__name__)


class CalibrationReader:
    """Loads sensor calibration data from a JSON file."""

    def __init__(self, cal_file: str) -> None:
        self.cal_file = cal_file
        self.data = {}
        logger.debug("CalibrationReader initialised: %s", cal_file)
        self.load()

    def load(self) -> None:
        """Load calibration data, raising typed exceptions on failure."""
        if not os.path.exists(self.cal_file):
            logger.error("Calibration file not found: %s", self.cal_file)
            raise CalibrationFileNotFoundError(self.cal_file)
        try:
            with open(self.cal_file, 'r') as f:
                self.data = json.load(f)
            logger.info("Calibration loaded: %s (%d keys)", self.cal_file, len(self.data))
        except json.JSONDecodeError as e:
            logger.error("Parse error in %s: %s", self.cal_file, e)
            raise CalibrationParseError(self.cal_file, str(e)) from e

    def validate(self) -> None:
        """Validate calibration data, raising CalibrationValidationError if invalid."""
        errors = []
        if 'sensor_name' not in self.data:
            errors.append("Missing required field: sensor_name")
        if 'channels' in self.data:
            if not isinstance(self.data['channels'], int):
                errors.append("channels must be an integer")
            elif self.data['channels'] <= 0:
                errors.append("channels must be greater than zero")
        if errors:
            logger.warning("Validation failed with %d error(s)", len(errors))
            raise CalibrationValidationError(errors)
        logger.debug("Calibration validation passed")

class ConfigurationManager():

    """Manages robot configurations from files."""

    def __init__(self, config_file):
        """Initialize with configuration file path."""
        self.config_file = config_file
        self.config = self.load()
        self.data = config_file
        self.load()

    def load(self):
        """Load configuration from file (auto-detect format)."""
        with open('json_robot_config.json', 'r') as file:
            config_data = json.load(file)
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
        errors = []

        # Check required fields exist
        if 'sensor_name' not in self.data:
            errors.append("Missing required field: sensor_name")

        # Check data types
        if 'channels' in self.data:
            if not isinstance(self.data['channels'], int):
                errors.append("channels must be integer")
            elif self.data['channels'] <= 0:
                errors.append("channels must be greater than zero")

        # Raise with all errors at once — don't stop at the first failure
        if errors:
            raise CalibrationValidationError(errors)
        
        # Check required fields exist
        # Check data types are correct
        # Check values are in valid ranges
        # Raise ConfigValidationError with all errors if any fail

class LineFollowerRobot:
    """Focuses only on behavior."""

    def __init__(self, name, ir_sensors):
        self.name = name
        self.ir_sensors = ir_sensors

    def read_ir_sensors(self):
        """Behavior - independent of how config was loaded"""
        return [0 if i % 2 == 0 else 1 for i in range(self.ir_sensors)]

# Usage: Separate concerns
config_manager = ConfigurationManager('json_robot_config.json')
robot = LineFollowerRobot(
    name=config_manager.get('name'),
    ir_sensors=config_manager.get('sensors.ir_count')
)
config_manager.validate()

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