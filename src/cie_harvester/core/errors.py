class HarvesterError(Exception):
    """Base error for the harvester."""


class ConfigError(HarvesterError):
    """Raised for invalid configuration."""


class SourceError(HarvesterError):
    """Raised for source registry or git failures."""


class ValidationError(HarvesterError):
    """Raised when a pack or schema check fails."""
