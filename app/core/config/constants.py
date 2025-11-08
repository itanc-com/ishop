"""
Application constants - READONLY values.
These are hardcoded and should NOT be modified via environment variables.
"""
from typing import Final

# ============================================================================
# API CONSTANTS
# ============================================================================
API_V1_PREFIX: Final[str] = "/v1"
AUTH_TOKEN_SWAGGER: Final[str] = f"{API_V1_PREFIX}/auth/token/swagger"
