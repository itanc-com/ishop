"""
Configuration module for the application.
Exports settings and constants for easy import.
"""
from .constants import (
    API_V1_PREFIX,
    AUTH_TOKEN_SWAGGER,
)
from .settings import EnvironmentType, settings

__all__ = [
    # Settings
    "settings",
    "EnvironmentType",
    # Constants
    "API_V1_PREFIX",
    "AUTH_TOKEN_SWAGGER",
]
