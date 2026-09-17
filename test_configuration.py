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